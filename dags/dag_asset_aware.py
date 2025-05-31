from airflow.models import Variable
from airflow.sdk import Asset, dag, task


dbt_env = Variable.get("dbt_env", default_var="dev").lower()

if dbt_env not in ("dev", "prod"):
    raise ValueError(f"dbt_env inválido: {dbt_env!r}, use 'dev' ou 'prod'")

asset_name_dev = 'postgres://host.docker.internal:5433/postgres/public/stg_cadastros_2'
asset_name_prod = 'postgres://yamanote.proxy.rlwy.net:32322/railway/public/stg_cadastros_2'

asset_name = asset_name_dev if dbt_env == "dev" else asset_name_prod

asset_tabela = Asset(
    name=asset_name,
    uri=asset_name,
    group='asset'
)

@dag(schedule=[asset_tabela])
def new_asset():
    @task
    def print_asset(asset_name):
        print("Asset: ", asset_name)
    print_asset(asset_tabela)

new_asset()