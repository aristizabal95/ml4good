import torch
from torch.optim.lr_scheduler import ExponentialLR
import wandb
import optuna

from ml4good.hyperparameters.model import make_net93
from ml4good.hyperparameters.processing.loader import CifarLoader
from ml4good.hyperparameters.config.core import config, DATASET_DIR
from ml4good.hyperparameters.train import train

# Initialize wandb for the hyperparameter search
wandb.init(
    project="ml4good-hyperparameters",
    name="hyperparameter-search",
    config={
        "search_algorithm": "optuna",
        "n_trials": 100,
        "direction": "maximize"
    }
)

# 1. Define an objective function to be maximized.
def objective(trial):
    # Use CUDA if available, otherwise use CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # 2. Suggest values of the hyperparameters using a trial object.
    block1_width = trial.suggest_int('block1_width', 8, 128)
    block2_width = trial.suggest_int('block2_width', 8, 128)
    block3_width = trial.suggest_int('block3_width', 8, 128)
    widths = {
        'block1': block1_width,
        'block2': block2_width,
        'block3': block3_width
    }
    batchnorm_momentum = trial.suggest_float('batchnorm_momentum', 0.1, 0.9)
    scaling_factor = trial.suggest_float('scaling_factor', 0.1, 2.0)
    batch_size = trial.suggest_int('batch_size', 16, 256)
    learning_rate = trial.suggest_float('learning_rate', 1e-5, 1e1, log=True)
    lr_decay = trial.suggest_float('lr_decay', 0.1, 0.9)
    weight_decay = trial.suggest_float('weight_decay', 1e-5, 1e-1, log=True)
    augmentations = config.train_config.augmentations

    # Log trial parameters to wandb
    trial_params = {
        "trial_number": trial.number,
        "block1_width": block1_width,
        "block2_width": block2_width,
        "block3_width": block3_width,
        "batchnorm_momentum": batchnorm_momentum,
        "scaling_factor": scaling_factor,
        "batch_size": batch_size,
        "learning_rate": learning_rate,
        "lr_decay": lr_decay,
        "weight_decay": weight_decay
    }
    wandb.log(trial_params)

    model = make_net93(widths, batchnorm_momentum, scaling_factor)
    train_loader = CifarLoader(
        DATASET_DIR, 
        train=True, 
        batch_size=batch_size, 
        aug=augmentations
    )
    val_loader = CifarLoader(
        DATASET_DIR, 
        train=False, 
        batch_size=batch_size, 
        aug=augmentations
    )
    
    # Define loss function and optimizer
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(
        model.parameters(), 
        lr=learning_rate, 
        weight_decay=weight_decay
    )
    scheduler = ExponentialLR(optimizer, gamma=(1-lr_decay))
    schedulers = [scheduler]
    
    # Move model and loss function to device
    model = model.to(device).half()
    loss_fn = loss_fn.to(device)

    final_val_acc = train(
        model, 
        optimizer, 
        schedulers, 
        loss_fn, 
        train_loader, 
        val_loader, 
        num_epochs=2,
        device=device
    )
    
    # Log trial result to wandb
    wandb.log({
        "trial_number": trial.number,
        "final_val_accuracy": final_val_acc
    })
    
    return final_val_acc

# 3. Create a study object and optimize the objective function.
study = optuna.create_study(direction='maximize')
study.optimize(objective, n_trials=100)

# Log best trial results to wandb
best_trial = study.best_trial
wandb.log({
    "best_trial_number": best_trial.number,
    "best_val_accuracy": best_trial.value,
    "best_params": best_trial.params
})

# Finish wandb run
wandb.finish()