import os
import yaml
from dotenv import load_dotenv
from pathlib import Path
from typing import Any, Dict


class Configuration:
    def __init__(self, yaml_file: str = "app/config/config.yaml"):
        self._config_data: Dict[str, Any] = {}
        self.yaml_file = yaml_file
        self._load_yaml_config()
        self._load_environment_variables()
        self._dict_to_attr(self._config_data)

    def _load_yaml_config(self) -> None:
        yaml_path = Path(self.yaml_file)
        if not yaml_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.yaml_file}")

        try:
            with open(yaml_path, "r") as stream:
                self._config_data = yaml.safe_load(stream) or {}
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML config: {e}")

    def _load_environment_variables(self) -> None:
        # Try multiple possible .env locations
        possible_env_paths = [
            Path(__file__).parent.parent / ".env",
            Path(__file__).parent.parent.parent / ".env",
            Path.cwd() / ".env"
        ]
        
        for env_path in possible_env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                break

        # Environment overrides
        env_config = {
            'FLASK_ENV': ('env.FLASK_ENV', os.getenv('FLASK_ENV')),
            'SECRET_KEY': ('env.SECRET_KEY', os.getenv('SECRET_KEY')),
            'DEBUG': ('env.DEBUG', os.getenv('DEBUG')),
            'DATABASE_URL': ('database.url', os.getenv('DATABASE_URL')),
        }

        for env_var, (config_path, value) in env_config.items():
            if value is not None:
                self._set_nested_config(config_path, value)

    def _set_nested_config(self, path: str, value: Any) -> None:
        keys = path.split('.')
        config = self._config_data

        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]

        config[keys[-1]] = value

    def _dict_to_attr(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            attr_name = key.upper()
            if isinstance(value, dict):
                namespace = type('ConfigNamespace', (), {})()
                self._dict_to_attr_on_obj(namespace, value)
                setattr(self, attr_name, namespace)
            else:
                setattr(self, attr_name, value)

    def _dict_to_attr_on_obj(self, obj: object, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            attr_name = key.upper()
            if isinstance(value, dict):
                namespace = type('ConfigNamespace', (), {})()
                self._dict_to_attr_on_obj(namespace, value)
                setattr(obj, attr_name, namespace)
            else:
                setattr(obj, attr_name, value)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self._config_data

        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default


# Global configuration instance
cfg = Configuration()