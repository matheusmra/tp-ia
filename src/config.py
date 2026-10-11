"""Configuracoes globais, caminhos, nomes de colunas e mapeamentos para o dataset NSL-KDD."""

from pathlib import Path

# Diretorios principais do projeto
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"

# Caminhos dos arquivos de treino e teste
TRAIN_FILE_RAW = RAW_DATA_DIR / "KDDTrain+.txt"
TEST_FILE_RAW = RAW_DATA_DIR / "KDDTest+.txt"

# Semente pseudoaleatoria para reprodutibilidade estrita
RANDOM_STATE = 42

# Nomes oficiais das 41 features descritivas da base NSL-KDD
FEATURE_NAMES = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "land",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate",
    "dst_host_count",
    "dst_host_srv_count",
    "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate",
    "dst_host_same_src_port_rate",
    "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate",
    "dst_host_srv_serror_rate",
    "dst_host_rerror_rate",
    "dst_host_srv_rerror_rate",
]

# Coluna alvo (tipo de ataque ou normal)
LABEL_NAME = "label"

# Atributo de pontuacao de dificuldade (especifico do NSL-KDD original)
# AVISO: Nao deve ser usado como feature descritiva nos modelos para evitar vazamento de dados (data leakage)!
DIFFICULTY_NAME = "difficulty_level"

# Todas as 43 colunas presentes no arquivo bruto
ALL_COLUMNS = FEATURE_NAMES + [LABEL_NAME, DIFFICULTY_NAME]

# Tipos de atributos
CATEGORICAL_FEATURES = ["protocol_type", "service", "flag"]
NUMERICAL_FEATURES = [col for col in FEATURE_NAMES if col not in CATEGORICAL_FEATURES]

# Atributos com variancia zero identificados no conjunto de treino
# 'num_outbound_cmds' possui valor constante 0 em todas as 125.973 linhas de treino
ZERO_VARIANCE_FEATURES = ["num_outbound_cmds"]

# Mapeamento oficial dos 40 tipos de ataque observados em treino e teste para as 5 superclasses canonicas
# Categorias: normal, dos (Denial of Service), probe, r2l (Remote to Local), u2r (User to Root)
ATTACK_MAPPING = {
    # Normal
    "normal": "normal",
    # DoS
    "apache2": "dos",
    "back": "dos",
    "land": "dos",
    "mailbomb": "dos",
    "neptune": "dos",
    "pod": "dos",
    "processtable": "dos",
    "smurf": "dos",
    "teardrop": "dos",
    "udpstorm": "dos",
    "worm": "dos",
    # Probe
    "ipsweep": "probe",
    "mscan": "probe",
    "nmap": "probe",
    "portsweep": "probe",
    "saint": "probe",
    "satan": "probe",
    # R2L
    "ftp_write": "r2l",
    "guess_passwd": "r2l",
    "httptunnel": "r2l",
    "imap": "r2l",
    "multihop": "r2l",
    "named": "r2l",
    "phf": "r2l",
    "sendmail": "r2l",
    "snmpgetattack": "r2l",
    "snmpguess": "r2l",
    "spy": "r2l",
    "warezclient": "r2l",
    "warezmaster": "r2l",
    "xlock": "r2l",
    "xsnoop": "r2l",
    # U2R
    "buffer_overflow": "u2r",
    "loadmodule": "u2r",
    "perl": "u2r",
    "ps": "u2r",
    "rootkit": "u2r",
    "sqlattack": "u2r",
    "xterm": "u2r",
}

# Ordem padronizada das classes para relatorios e matrizes de confusao
CLASSES_5 = ["normal", "dos", "probe", "r2l", "u2r"]
