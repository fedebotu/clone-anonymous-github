import os


# Default configuration
DEFAULT_CONFIG = {'url': 'https://anonymous.4open.science/r/840c8c57-3c32-451e-bf12-0e20be300389/',
                    'save_dir': os.getcwd(),
                    'max_conns': 256,
                    'max_retry': 5}


def load_config():
    """Load configuration"""
    return DEFAULT_CONFIG


def get_config_from_values(values):
    """Config from PySimpleGUI values"""
    config = DEFAULT_CONFIG.copy()
    for key in config.keys():
        try:
            value = values[key]
            config[key] = value
        except Exception as e:
            print("Could not get config from values:", e)
            continue
    return config