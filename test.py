def validate_vault_approle_access(vault_addr: str, role_id: str, secret_id: str, test_secret_path: str):
    """
    Validates that AppRole credentials can access a Vault secret.

    :param vault_addr: Vault server URL
    :param role_id: Vault AppRole role_id
    :param secret_id: Vault AppRole secret_id
    :param test_secret_path: Path to any readable secret to test access
    """
    LOG.info("Validating Vault AppRole access to: %s", test_secret_path)
    try:
        client = hvac.Client(url=vault_addr)
        client.auth.approle.login(role_id=role_id, secret_id=secret_id)

        if not client.is_authenticated():
            LOG.error("AppRole authentication failed. Check role_id or secret_id.")
            raise PermissionError("Vault AppRole authentication failed")

        # Try accessing the test secret
        client.secrets.kv.v2.read_secret_version(path=test_secret_path)
        LOG.info("✅ Vault access validation successful.")
    except hvac.exceptions.Forbidden:
        LOG.error("❌ Vault AppRole credentials are invalid or lack permission to access: %s", test_secret_path)
        raise
    except Exception as e:
        LOG.error("❌ Unexpected error during Vault access validation: %s", str(e))
        raise



validate_vault_approle_access(
    vault_addr='https://vaultops.rtv.corp.nodalx.net',
    role_id=os.environ['VAULT_ROLE_ID'],
    secret_id=os.environ['VAULT_SECRET_ID'],
    test_secret_path='nodalsuite/qa13/kv/rabbitmq/admin'
)
