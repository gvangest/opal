from opal_common.logger import logger
from opal_common.schemas.policy_source import (
    GitPolicyScopeSource,
    NoAuthData,
    SSHAuthData,
)
from opal_common.schemas.scopes import Scope
from opalserver.config import ServerRole, opalserver_config
from opalserver.scopes.scope_repository import ScopeRepository

DEFAULT_SCOPE_ID = "default"


async def load_scopes(repo: ScopeRepository):
    if opalserver_config.SERVER_ROLE == ServerRole.Primary:
        logger.info("Server is primary, loading default scope.")
        await _load_env_scope(repo)


async def _load_env_scope(repo: ScopeRepository):
    # backwards compatible opal scope
    if opalserver_config.POLICY_REPO_URL is not None:
        logger.info(
            "Adding default scope from env: {url}",
            url=opalserver_config.POLICY_REPO_URL,
        )

        auth = NoAuthData()

        if opalserver_config.POLICY_REPO_SSH_KEY is not None:
            private_ssh_key = opalserver_config.POLICY_REPO_SSH_KEY
            private_ssh_key = private_ssh_key.replace("_", "\n")

            if not private_ssh_key.endswith("\n"):
                private_ssh_key += "\n"

            auth = SSHAuthData(username="git", private_key=private_ssh_key)

        scope = Scope(
            scope_id=DEFAULT_SCOPE_ID,
            policy=GitPolicyScopeSource(
                source_type=opalserver_config.POLICY_SOURCE_TYPE.lower(),
                url=opalserver_config.POLICY_REPO_URL,
                manifest=opalserver_config.POLICY_REPO_MANIFEST_PATH,
                branch=opalserver_config.POLICY_REPO_MAIN_BRANCH,
                auth=auth,
            ),
        )

        await repo.put(scope)
