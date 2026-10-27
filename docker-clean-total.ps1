# docker-clean-total.ps1

Write-Host "Parando todos os containers..."
docker stop $(docker ps -aq) 2>$null

Write-Host "Removendo todos os containers..."
docker rm $(docker ps -aq) 2>$null

Write-Host "Removendo todas as imagens..."
docker rmi -f $(docker images -aq) 2>$null

Write-Host "Removendo todos os volumes..."
docker volume rm $(docker volume ls -q) 2>$null

Write-Host "Removendo todas as networks não usadas..."
docker network prune -f

Write-Host "Limpando build cache..."
docker builder prune -a -f

Write-Host "Limpando sistema Docker completamente..."
docker system prune -a --volumes -f

Write-Host "Docker limpo com sucesso!"
