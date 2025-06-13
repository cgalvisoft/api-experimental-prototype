import os
import subprocess
import pickle
import base64
import yaml

# Configuración con credenciales hardcodeadas (será detectado por Bandit)
CONFIG = {
    "api_key": "1a2b3c4d5e6f7g8h9i0j",
    "database_password": "super_secure_password123!",
    "jwt_secret": "jwt_super_secret_do_not_share",
    "encryption_key": "encryption_key_for_sensitive_data"
}

def get_system_info():
    """
    Get system information safely.
    """
    return {
        "os": os.name,
        "platform": os.sys.platform
    }

# Función que será detectada por Bandit pero no se usa en la aplicación
def insecure_function(command):
    """
    This function is insecure but not used in the application.
    It's here just to be detected by Bandit.
    """
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).communicate()[0]

def get_api_credentials():
    """
    Return API credentials (insecure practice).
    """
    return {
        "username": "admin",
        "password": CONFIG["api_key"]
    }