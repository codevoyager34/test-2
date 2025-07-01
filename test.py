def get_vault_auth_params(env: str) -> dict:
    """
    Get Vault AppRole credentials and vault address from CMDB for a given environment.
    :param env: environment like 'QA13'
    :return: dict with keys: vault_addr, role_id, secret_id
    """
    query = """
        SELECT property_name, property_value
        FROM vault_credentials
        WHERE environment = %s
    """
    user_dict = get_username_and_password(env)
    conn_string = "host={host} port={port} dbname={dbname} user={user} password={password}".format(
        host=os.environ['CMDB_HOST'],
        port=os.environ['CMDB_PORT'],
        dbname=os.environ['CMDB_DATABASE'],
        user=user_dict['username'],
        password=user_dict['password']
    )

    with autocommit_cursor(conn_string) as cursor:
        cursor.execute(query, (env,))
        results = {row[0]: row[1] for row in cursor.fetchall()}

    return {
        "vault_addr": results.get("vault.addr"),
        "role_id": results.get("vault.role_id"),
        "secret_id": results.get("vault.secret_id")
    }



def validate_vault_access_for_env(env: str, mount_point: str, secret_path: str):
    """
    Looks up Vault credentials from CMDB and validates access to a path.
    """
    creds = get_vault_auth_params(env)
    if not creds["vault_addr"] or not creds["role_id"] or not creds["secret_id"]:
        raise ValueError(f"Missing Vault credentials in CMDB for environment: {env}")

    validate_vault_approle_access(
        vault_addr=creds["vault_addr"],
        role_id=creds["role_id"],
        secret_id=creds["secret_id"],
        mount_point=mount_point,
        secret_path=secret_path
    )



validate_vault_access_for_env(
    env="QA13",
    mount_point="nodalsuite/qa13/kv",
    secret_path="rabbitmq/admin"
)
