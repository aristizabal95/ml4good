import torch
import torch.nn.functional as F
from torch.optim.lr_scheduler import ExponentialLR
import wandb

from ml4good.hyperparameters.processing.loader import CifarLoader
from ml4good.hyperparameters.model import make_net93
from ml4good.hyperparameters.config.core import config, DATASET_DIR

def infer(model, loader, tta_level=0):
    
    def infer_basic(inputs, net):
        return net(inputs).clone()

    def infer_mirror(inputs, net):
        return 0.5 * net(inputs) + 0.5 * net(inputs.flip(-1))

    def infer_mirror_translate(inputs, net):
        logits = infer_mirror(inputs, net)
        pad = 1 
        padded_inputs = F.pad(inputs, (pad,)*4, 'reflect')
        inputs_translate_list = [ 
            padded_inputs[:, :, 0:32, 0:32],
            padded_inputs[:, :, 2:34, 2:34],
        ]   
        logits_translate_list = [infer_mirror(inputs_translate, net)
                                 for inputs_translate in inputs_translate_list]
        logits_translate = torch.stack(logits_translate_list).mean(0)
        return 0.5 * logits + 0.5 * logits_translate

    model.eval()
    test_images = loader.normalize(loader.images)
    infer_fn = [infer_basic, infer_mirror, infer_mirror_translate][tta_level]
    with torch.no_grad():
        return torch.cat([infer_fn(inputs, model) for inputs in test_images.split(2000)])

def evaluate(model, loader, tta_level=0):
    logits = infer(model, loader, tta_level)
    return (logits.argmax(1) == loader.labels).float().mean().item()

def train(model, optim, schedulers, loss_fn, train_loader, val_loader, num_epochs):
    losses = []
    best_val_accuracy = 0
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, labels in train_loader:
            optim.zero_grad()
            outputs = model(inputs)
            loss = loss_fn(outputs, labels)
            loss.backward()
            optim.step()

            running_loss += loss.item()
            predicted = F.softmax(outputs, dim=1).argmax(dim=1)
            total += labels.size(0)
            correct += predicted.eq(labels).sum().item()

        losses.append(running_loss)
        for scheduler in schedulers:
            scheduler.step()
        
        train_loss = running_loss / len(train_loader)
        train_accuracy = 100 * correct / total
        current_lr = optim.param_groups[0]["lr"]
        
        print(f'Learning rate: {current_lr}')
        print(f'Epoch {epoch + 1}/{num_epochs}, Loss: {train_loss}, Accuracy: {train_accuracy}')

        # Validation phase
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0

        with torch.no_grad():
            for inputs, labels in val_loader:
                outputs = model(inputs)
                loss = loss_fn(outputs, labels)

                val_loss += loss.item()
                predicted = F.softmax(outputs, dim=1).argmax(dim=1) 
                val_total += labels.size(0)
                val_correct += predicted.eq(labels).sum().item()

        val_loss = val_loss / len(val_loader)
        val_accuracy = 100 * val_correct / val_total

        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            torch.save(model.state_dict(), f'best_model.pth')
        
        print(f'Validation Loss: {val_loss}, Validation Accuracy: {val_accuracy}')
        
        # Log metrics to wandb
        wandb.log({
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "val_loss": val_loss,
            "val_accuracy": val_accuracy,
            "learning_rate": current_lr
        })
        
    return val_accuracy

def main():
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    device = "cuda" if torch.cuda.is_available() else device
    # device = "cpu"
    print(f"Using device: {device}")

    train_config = config.train_config
    net_config = config.net_config

    # Initialize wandb
    wandb.init(
        project="ml4good-hyperparameters",
        config={
            "learning_rate": train_config.learning_rate,
            "batch_size": train_config.batch_size,
            "epochs": train_config.epochs,
            "weight_decay": train_config.weight_decay,
            "lr_decay": train_config.lr_decay,
            "widths": net_config.widths,
            "batchnorm_momentum": net_config.batchnorm_momentum,
            "scaling_factor": net_config.scaling_factor,
            "augmentations": train_config.augmentations
        }
    )

    model = make_net93(net_config.widths, net_config.batchnorm_momentum, net_config.scaling_factor)
    # Create data loaders
    train_loader = CifarLoader(DATASET_DIR, train=True, batch_size=train_config.batch_size, aug=train_config.augmentations, device=device)
    val_loader = CifarLoader(DATASET_DIR, train=False, batch_size=train_config.batch_size, aug=train_config.augmentations, device=device)
    # Define loss function and optimizer
    loss_fn = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.SGD(model.parameters(), lr=train_config.learning_rate, weight_decay=train_config.weight_decay)
    scheduler = ExponentialLR(optimizer, gamma=(1-train_config.lr_decay))
    schedulers = [scheduler]
    # Move model to device
    model.to(device).half()
    
    # Log model architecture to wandb
    wandb.watch(model, log="all")
    
    # Train the model
    train(model, optimizer, schedulers, loss_fn, train_loader, val_loader, train_config.epochs)
    
    # Finish wandb run
    wandb.finish()

if __name__ == "__main__":
    main()