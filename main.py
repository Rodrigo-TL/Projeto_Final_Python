from pathlib import Path

import matplotlib

# Permite salvar gráficos em arquivos sem abrir janelas na tela.
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


# Localiza o CSV na pasta indicada na estrutura do seu PyCharm.
PASTA_PROJETO = Path(__file__).resolve().parent
NOME_CSV = "funcionarios - funcionarios.csv"
CAMINHO_CSV = PASTA_PROJETO / "Projeto Final Python" / NOME_CSV

# Se o arquivo estiver ao lado do main.py, também tenta encontrá-lo ali.
if not CAMINHO_CSV.exists():
    CAMINHO_CSV = PASTA_PROJETO / NOME_CSV

PASTA_RESULTADOS = PASTA_PROJETO / "resultados"


# Encerra com uma mensagem clara se o CSV não estiver nos locais esperados.
if not CAMINHO_CSV.exists():
    raise FileNotFoundError(
        f"Arquivo não encontrado: {NOME_CSV}\n"
        "Coloque o CSV dentro da pasta 'Projeto Final Python' "
        "ou ao lado do main.py."
    )


# Carrega o CSV. Cada linha é uma fotografia semestral de um funcionário.
df = pd.read_csv(CAMINHO_CSV, sep=",", encoding="utf-8", low_memory=False)

print("1. INSPEÇÃO INICIAL")
print(f"Arquivo lido: {CAMINHO_CSV}")
print(f"Quantidade de registros: {len(df):,}")
print(f"Quantidade de colunas: {len(df.columns)}")
print("\nTipos de dados originais:")
print(df.dtypes.to_string())

print("\nValores ausentes:")
valores_ausentes = df.isna().sum()
print(valores_ausentes[valores_ausentes > 0].to_string())


# Verifica se o CSV contém as colunas usadas nas análises abaixo.
colunas_necessarias = [
    "id_registro",
    "id_funcionario",
    "nome_funcionario",
    "idade",
    "sexo",
    "escolaridade",
    "departamento",
    "cargo",
    "nivel_hierarquico",
    "salario",
    "data_admissao",
    "data_desligamento",
    "data_referencia",
    "tipo_contrato",
    "modalidade_trabalho",
    "avaliacao_desempenho",
    "horas_treinamento",
    "quantidade_promocoes",
    "status_funcionario",
]

colunas_faltantes = [
    coluna for coluna in colunas_necessarias if coluna not in df.columns
]

if colunas_faltantes:
    raise ValueError(f"Colunas não encontradas no CSV: {colunas_faltantes}")


print("\n2. LIMPEZA E PREPARAÇÃO DOS DADOS")

# Transforma números que vieram como texto em valores numéricos.
# Se algum valor não puder ser convertido, ele será tratado como ausente.
colunas_numericas = [
    "idade",
    "nivel_hierarquico",
    "salario",
    "avaliacao_desempenho",
    "horas_treinamento",
    "quantidade_promocoes",
]

for coluna in colunas_numericas:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

# Converte as datas para que possam ser ordenadas e agrupadas por ano.
colunas_de_data = [
    "data_admissao",
    "data_desligamento",
    "data_referencia",
]

for coluna in colunas_de_data:
    df[coluna] = pd.to_datetime(df[coluna], errors="coerce")

# Remove apenas registros repetidos com o mesmo identificador de linha.
# Não removemos repetições de id_funcionario: são snapshots de períodos diferentes.
registros_antes = len(df)
df = df.drop_duplicates(subset="id_registro")
duplicados_removidos = registros_antes - len(df)

# Idades abaixo de 18 ou acima de 100 são consideradas inválidas.
# Primeiro usamos a mediana das idades válidas da mesma pessoa.
df.loc[~df["idade"].between(18, 100), "idade"] = pd.NA
mediana_por_funcionario = df.groupby("id_funcionario")["idade"].transform("median")
df["idade"] = df["idade"].fillna(mediana_por_funcionario)

# Se todas as idades de uma pessoa forem inválidas, usamos a mediana geral.
df["idade"] = df["idade"].fillna(df["idade"].median())

# Preenche campos textuais vazios com uma indicação explícita.
# Datas de desligamento vazias são mantidas: podem indicar que não há data de saída.
colunas_textuais = [
    "nome_funcionario",
    "sexo",
    "escolaridade",
    "departamento",
    "cargo",
    "tipo_contrato",
    "modalidade_trabalho",
    "status_funcionario",
]

for coluna in colunas_textuais:
    df[coluna] = df[coluna].fillna("Não informado").astype(str).str.strip()

df["status_funcionario"] = df["status_funcionario"].str.capitalize()

print(f"Registros repetidos removidos: {duplicados_removidos}")
print(
    "Observação: o mesmo funcionário pode aparecer em várias linhas "
    "porque a base contém fotografias semestrais."
)


# Seleciona o snapshot mais recente para descrever a situação da empresa
# naquela data específica.
data_mais_recente = df["data_referencia"].max()
snapshot_atual = df[df["data_referencia"] == data_mais_recente].copy()

# Seleciona o último registro disponível de cada funcionário.
# Esta visão histórica pode incluir pessoas sem registro no snapshot mais recente.
ultimo_registro_por_funcionario = (
    df.sort_values("data_referencia")
    .drop_duplicates(subset="id_funcionario", keep="last")
    .copy()
)

funcionarios_ativos = snapshot_atual[
    snapshot_atual["status_funcionario"] == "Ativo"
].copy()


print("\n3. PERFIL NO SNAPSHOT MAIS RECENTE")
print(f"Data do snapshot: {data_mais_recente:%d/%m/%Y}")
print(
    "Funcionários registrados nesse snapshot: "
    f"{snapshot_atual['id_funcionario'].nunique():,}"
)
print(
    "Funcionários ativos nesse snapshot: "
    f"{funcionarios_ativos['id_funcionario'].nunique():,}"
)
print(
    "Total de funcionários distintos no histórico: "
    f"{df['id_funcionario'].nunique():,}"
)
print(f"Idade média no snapshot mais recente: {snapshot_atual['idade'].mean():.1f} anos")

print("\nFuncionários por departamento no snapshot mais recente:")
print(
    snapshot_atual.groupby("departamento")["id_funcionario"]
    .nunique()
    .sort_values(ascending=False)
    .to_string()
)

print("\nFuncionários por sexo no snapshot mais recente:")
print(
    snapshot_atual.groupby("sexo")["id_funcionario"]
    .nunique()
    .sort_values(ascending=False)
    .to_string()
)


print("\n4. SALÁRIOS DOS FUNCIONÁRIOS ATIVOS")
salario_por_departamento = (
    funcionarios_ativos.groupby("departamento")["salario"]
    .mean()
    .sort_values(ascending=False)
)

print("Salário médio por departamento:")
print(salario_por_departamento.round(2).to_string())

print("\nSalário médio por nível hierárquico:")
print(
    funcionarios_ativos.groupby("nivel_hierarquico")["salario"]
    .mean()
    .sort_index()
    .round(2)
    .to_string()
)


print("\n5. SITUAÇÃO FUNCIONAL")
print("Status no snapshot mais recente:")
status_atual = snapshot_atual["status_funcionario"].value_counts()
print(status_atual.to_string())

# Esta proporção descreve a composição do snapshot, não a rotatividade anual.
quantidade_desligados = status_atual.get("Desligado", 0)
percentual_desligados = quantidade_desligados / len(snapshot_atual) * 100

print(
    "Proporção de registros classificados como desligados nesse snapshot: "
    f"{percentual_desligados:.2f}%"
)

print("\nÚltimo status registrado para cada funcionário no histórico:")
print(
    ultimo_registro_por_funcionario["status_funcionario"]
    .value_counts()
    .to_string()
)


print("\n6. ADMISSÕES POR ANO")

# Cada funcionário é contado uma vez, mesmo que apareça em vários snapshots.
funcionarios_admissao = (
    df[["id_funcionario", "data_admissao"]]
    .drop_duplicates(subset="id_funcionario")
    .copy()
)

admissoes_por_ano = (
    funcionarios_admissao.groupby(funcionarios_admissao["data_admissao"].dt.year)[
        "id_funcionario"
    ]
    .nunique()
    .sort_index()
)

print(admissoes_por_ano.to_string())


print("\n7. TREINAMENTO E DESEMPENHO")
print(
    "Avaliação média dos ativos no snapshot mais recente: "
    f"{funcionarios_ativos['avaliacao_desempenho'].mean():.2f}"
)
print(
    "Horas médias de treinamento dos ativos no snapshot mais recente: "
    f"{funcionarios_ativos['horas_treinamento'].mean():.1f}"
)

# Divide as horas de treinamento em faixas para comparar as avaliações médias.
faixas_treinamento = [0, 10, 20, 30, float("inf")]
nomes_faixas = ["0–10 horas", "11–20 horas", "21–30 horas", "Mais de 30 horas"]

funcionarios_ativos["faixa_treinamento"] = pd.cut(
    funcionarios_ativos["horas_treinamento"],
    bins=faixas_treinamento,
    labels=nomes_faixas,
    include_lowest=True,
)

avaliacao_por_treinamento = (
    funcionarios_ativos.groupby("faixa_treinamento", observed=False)[
        "avaliacao_desempenho"
    ]
    .mean()
)

print("\nAvaliação média por faixa de treinamento:")
print(avaliacao_por_treinamento.round(2).to_string())
print(
    "Interpretação: a comparação mostra diferenças entre grupos, "
    "mas não prova que o treinamento cause mudança na avaliação."
)


print("\n8. EVOLUÇÃO DOS SNAPSHOTS")

# Conta pessoas distintas em cada fotografia semestral.
evolucao = (
    df.groupby("data_referencia")
    .agg(
        funcionarios=("id_funcionario", "nunique"),
        ativos=(
            "status_funcionario",
            lambda coluna: (coluna == "Ativo").sum(),
        ),
    )
    .sort_index()
)

print(evolucao.to_string())


print("\n9. GRÁFICOS")

# Cria a pasta de resultados caso ainda não exista.
PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

# Gráfico 1: evolução do quadro nos snapshots semestrais.
figura, eixo = plt.subplots(figsize=(10, 5))
evolucao[["funcionarios", "ativos"]].plot(marker="o", ax=eixo)
eixo.set_title("Evolução dos funcionários por snapshot")
eixo.set_xlabel("Data de referência")
eixo.set_ylabel("Número de funcionários")
eixo.grid(alpha=0.3)
figura.tight_layout()
figura.savefig(PASTA_RESULTADOS / "evolucao_funcionarios.png", dpi=150)
plt.close(figura)
print(
    "evolucao_funcionarios.png: compara o total de funcionários "
    "e os ativos ao longo dos snapshots."
)

# Gráfico 2: salário médio por departamento entre os funcionários ativos.
figura, eixo = plt.subplots(figsize=(9, 5))
salario_por_departamento.sort_values().plot(
    kind="barh",
    ax=eixo,
    color="#4472C4",
)
eixo.set_title("Salário médio por departamento — funcionários ativos")
eixo.set_xlabel("Salário médio (R$)")
eixo.set_ylabel("Departamento")
figura.tight_layout()
figura.savefig(PASTA_RESULTADOS / "salario_por_departamento.png", dpi=150)
plt.close(figura)
print(
    "salario_por_departamento.png: compara o salário médio "
    "entre departamentos."
)

# Gráfico 3: quantidade de admissões por ano.
figura, eixo = plt.subplots(figsize=(9, 5))
admissoes_por_ano.plot(kind="bar", ax=eixo, color="#70AD47")
eixo.set_title("Admissões por ano")
eixo.set_xlabel("Ano")
eixo.set_ylabel("Funcionários admitidos")
figura.tight_layout()
figura.savefig(PASTA_RESULTADOS / "admissoes_por_ano.png", dpi=150)
plt.close(figura)
print(
    "admissoes_por_ano.png: mostra em quais anos houve mais admissões."
)

# Gráfico 4: avaliação média em cada faixa de treinamento.
figura, eixo = plt.subplots(figsize=(9, 5))
avaliacao_por_treinamento.plot(
    kind="bar",
    ax=eixo,
    color="#ED7D31",
)
eixo.set_title("Avaliação média por faixa de treinamento")
eixo.set_xlabel("Horas de treinamento")
eixo.set_ylabel("Avaliação média")
eixo.tick_params(axis="x", rotation=20)
figura.tight_layout()
figura.savefig(PASTA_RESULTADOS / "treinamento_e_desempenho.png", dpi=150)
plt.close(figura)
print(
    "treinamento_e_desempenho.png: compara as avaliações médias "
    "entre faixas de treinamento."
)

# Gráfico 5: distribuição dos status no snapshot mais recente.
figura, eixo = plt.subplots(figsize=(8, 5))
status_atual.plot(kind="bar", ax=eixo, color="#5B9BD5")
eixo.set_title(f"Status dos funcionários em {data_mais_recente:%d/%m/%Y}")
eixo.set_xlabel("Status")
eixo.set_ylabel("Número de registros")
eixo.tick_params(axis="x", rotation=0)
figura.tight_layout()
figura.savefig(PASTA_RESULTADOS / "status_funcionarios.png", dpi=150)
plt.close(figura)
print(
    "status_funcionarios.png: mostra a distribuição dos status "
    "na data mais recente da base."
)


print("\n10. ESTUDO APLICADO")
print(
    "Pergunta gerencial: as avaliações médias diferem entre funcionários "
    "com diferentes quantidades de horas de treinamento?"
)
print(
    "Método: foram considerados os funcionários ativos no snapshot mais recente. "
    "As horas de treinamento foram divididas em faixas e comparadas com a "
    "avaliação média de cada grupo."
)
print("\nResultados:")
print(avaliacao_por_treinamento.round(2).to_string())
print(
    "\nConclusão: use as diferenças observadas como ponto de partida para "
    "investigações sobre treinamento e desempenho. Esta análise descritiva "
    "não demonstra relação de causa e efeito."
)


print("\nArquivos gerados na pasta:")
print(PASTA_RESULTADOS)