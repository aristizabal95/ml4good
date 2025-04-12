from pydantic import BaseModel
from pathlib import Path
from typing import Optional, Dict, Any
from strictyaml import YAML, load

from ml4good import hyperparameters

PACKAGE_ROOT = Path(hyperparameters.__file__).resolve().parent
CONFIG_FILE_PATH = PACKAGE_ROOT / "config.yml"
DATASET_DIR = PACKAGE_ROOT / "data"

class TrainConfig(BaseModel):
    """Model configuration class."""

    # Training parameters
    batch_size: int
    epochs: int
    learning_rate: float
    lr_decay: float
    weight_decay: float
    dropout: float
    augmentations: Dict[str, int]

    # Evaluation parameters
    eval_steps: int

class NetworkConfig(BaseModel):
    widths: Dict[str, int]
    batchnorm_momentum: float
    scaling_factor: float

class Config(BaseModel):
    train_config: TrainConfig
    net_config: NetworkConfig

def find_config_file() -> Path:
    if CONFIG_FILE_PATH.is_file():
        return CONFIG_FILE_PATH
    raise Exception(f"Config not found at {CONFIG_FILE_PATH}")

def fetch_config_from_yaml(cfg_path: Optional[Path] = None) -> YAML:
    """Parse YAML containing the package configuration"""
    if cfg_path is None:
        cfg_path = find_config_file()

    if cfg_path:
        with open(cfg_path, "r") as f:
            parsed_config = load(f.read())
            return parsed_config
    raise OSError(f"Did not find config file at: {cfg_path}")

def create_and_validate_config(parsed_config: YAML = None) -> Config:
    if parsed_config is None:
        parsed_config = fetch_config_from_yaml()

    _config = Config(
        train_config = TrainConfig(**parsed_config.data),
        net_config = NetworkConfig(**parsed_config.data)
    )

    return _config

config = create_and_validate_config()