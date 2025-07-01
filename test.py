def validate_vault_access_with_helper(vault_helper: VaultHelper, secret_path: str):
    """
    Validates that the VaultHelper's client can access the given Vault secret path.
    Does not return or log secret data — only verifies access.

    :param vault_helper: An initialized VaultHelper instance with AppRole auth
    :param secret_path: The full Vault path to check (e.g., 'nodalsuite/qa13/kv/rabbitmq/admin')
    :raises Exception: If access fails
    """
    LOG.info("Validating Vault access for path: %s", secret_path)
    try:
        client = vault_helper.vault_client
        # Attempt to read the secret (but don’t use or log it)
        client.secrets.kv.v2.read_secret_version(path=secret_path)
        LOG.info("✅ Vault access validation succeeded for path: %s", secret_path)
    except hvac.exceptions.Forbidden:
        LOG.error("❌ Access denied for Vault path: %s", secret_path)
        raise
    except Exception as e:
        LOG.error("❌ Vault validation error: %s", str(e))
        raise


vault = VaultHelper()
vault.init(environment="qa13", vault_addr="https://vaultops.rtv.corp.nodalx.net")


validate_vault_access_with_helper(
    vault_helper=vault,
    secret_path='nodalsuite/qa13/kv/rabbitmq/admin'
)
