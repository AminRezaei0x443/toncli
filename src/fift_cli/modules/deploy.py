import os

from colorama import Fore, Style
from requests import get as http_get

from .deploy_wallet_contract import DeployWalletContract
from .utils.conf import config_folder, config_uri
from .utils.log import logger

gr = Fore.GREEN
bl = Fore.BLUE
rs = Style.RESET_ALL


class Deployer:
    def __init__(self, network: str, update_config: bool = False, workchain: int = 0):
        logger.info(f"🚀 You want to {bl}deploy{rs} your contract to {gr}{network}{rs} - that's grate!")

        self.network: str = Deployer.get_network_config_path(network, update_config)
        self.project_root: str = os.getcwd()
        self.workchain = workchain # workchain deploy to

        # Check needed to deploy files
        if not self.check_for_needed_files_to_deploy():
            # If no - do nothing
            return

        self.deploy_contract = DeployWalletContract()

    def check_for_needed_files_to_deploy(self) -> bool:
        '''Check needed files and log if there is no one'''

        files = os.listdir(self.project_root)
        needed_files = ['data.fif', 'code.fc']

        for file in needed_files:
            if file not in files:
                logger.error(f"🚫 It is not project root, there is no {file} - I can't deploy it")
                return False

        return True

    @staticmethod
    def get_network_config_path(network: str, update_config: bool = False) -> str:

        filename = f"{network}.json"

        # Find file and return path to it
        if filename in os.listdir(config_folder) and not update_config:
            logger.info(f"🏗  Found config of {gr}{network}{rs} in {gr}{config_folder}{rs}")
        else:
            logger.info(
                f"🏗  Config of {gr}{network}{rs} will be downloaded to {gr}{config_folder}{rs} "
                f"from {gr}{config_uri[network]}{rs}")

            # need to download config file and save it
            r = http_get(config_uri[network], stream=True)
            if r.status_code == 200:
                with open(f"{config_folder}/{filename}", 'wb') as f:
                    for chunk in r:
                        f.write(chunk)

        return f"{config_folder}/{filename}"
