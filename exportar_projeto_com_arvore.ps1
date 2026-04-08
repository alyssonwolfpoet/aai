param(
    [string]$PastaProjeto = ".",
    [string]$ArquivoSaida = "projeto_completo.txt"
)

# Extensões que queremos incluir
$extensoes = @("*.py", "*.md", "*.txt", "*.json", "*.yaml", "*.yml", "*.ini", "*.cfg")

# Pastas a ignorar
$ignorarPastas = @(".git", "__pycache__", ".venv", "venv", "node_modules", ".idea", ".vscode")

# Limpa arquivo de saída se já existir
if (Test-Path $ArquivoSaida) {
    Remove-Item $ArquivoSaida
}

# ========================
# 🌳 GERAR ÁRVORE
# ========================
function Mostrar-Arvore {
    param (
        [string]$Caminho,
        [string]$Prefixo = ""
    )

    $itens = Get-ChildItem -Path $Caminho | Where-Object {
        $ignorarPastas -notcontains $_.Name
    }

    foreach ($item in $itens) {
        if ($item.PSIsContainer) {
            Add-Content $ArquivoSaida "$Prefixo📁 $($item.Name)"
            Mostrar-Arvore -Caminho $item.FullName -Prefixo "$Prefixo    "
        } else {
            Add-Content $ArquivoSaida "$Prefixo📄 $($item.Name)"
        }
    }
}

Add-Content $ArquivoSaida "================= 🌳 ESTRUTURA DO PROJETO ================="
Mostrar-Arvore -Caminho $PastaProjeto
Add-Content $ArquivoSaida "`n`n"

# ========================
# 📄 CONCATENAR ARQUIVOS
# ========================
$arquivos = Get-ChildItem -Path $PastaProjeto -Recurse -Include $extensoes -File | Where-Object {
    $caminho = $_.FullName
    -not ($ignorarPastas | ForEach-Object { $caminho -like "*$_*" } | Where-Object { $_ })
}

foreach ($arquivo in $arquivos) {
    Add-Content $ArquivoSaida "========================================"
    Add-Content $ArquivoSaida "ARQUIVO: $($arquivo.FullName)"
    Add-Content $ArquivoSaida "========================================"
    
    try {
        $conteudo = Get-Content $arquivo.FullName -Raw -ErrorAction Stop
        Add-Content $ArquivoSaida $conteudo
    } catch {
        Add-Content $ArquivoSaida "[ERRO AO LER ARQUIVO]"
    }

    Add-Content $ArquivoSaida "`n`n"
}

Write-Host "✔ Projeto exportado com árvore para: $ArquivoSaida"