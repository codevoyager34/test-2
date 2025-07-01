
def validate_vault_access_with_helper(vault_helper: VaultHelper, mount_point: str, secret_path: str):
    """
    Validates that the VaultHelper's client can access the given Vault secret path using KV v2.
    Does not return or log secrets — only confirms access.

    :param vault_helper: An initialized VaultHelper instance
    :param mount_point: The mount point of the KV engine (e.g., 'nodalsuite/qa13/kv')
    :param secret_path: The path under the mount point (e.g., 'rabbitmq/admin')
    """
    LOG.info("Validating Vault access at %s/%s", mount_point, secret_path)
    try:
        client = vault_helper.vault_client
        client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point,
            path=secret_path
        )
        LOG.info("✅ Vault access validation succeeded.")
    except hvac.exceptions.Forbidden:
        LOG.error("❌ Vault access denied at %s/%s", mount_point, secret_path)
        raise
    except Exception as e:
        LOG.error("❌ Vault access validation failed: %s", str(e))
        raise


validate_vault_access_with_helper(
    vault_helper=vault,
    mount_point="nodalsuite/qa13/kv",
    secret_path="rabbitmq/admin"
)
