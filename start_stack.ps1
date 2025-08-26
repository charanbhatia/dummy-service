Write-Host "🚀 Starting FastAPI Observability Stack" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if Docker is available
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Docker not found!" -ForegroundColor Red
    Write-Host "Please install Docker Desktop to run the full stack." -ForegroundColor Yellow
    exit 1
}

Write-Host "📦 Building and starting services..." -ForegroundColor Yellow

# Build and start all services
docker-compose up --build -d

Write-Host "⏳ Waiting for services to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 30

# Check if services are running
Write-Host "🔍 Checking service status..." -ForegroundColor Yellow

$services = @(
    @{name="FastAPI"; port=8000},
    @{name="Prometheus"; port=9090},
    @{name="Grafana"; port=3000},
    @{name="Jaeger"; port=16686},
    @{name="Loki"; port=3100}
)

foreach ($service in $services) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:$($service.port)" -TimeoutSec 5 -ErrorAction Stop
        Write-Host "✅ $($service.name) running on port $($service.port)" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ $($service.name) not responding on port $($service.port)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "🎉 Stack started successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📊 Access your services:" -ForegroundColor Cyan
Write-Host "  • FastAPI Application: http://localhost:8000" -ForegroundColor White
Write-Host "  • Grafana Dashboard:   http://localhost:3000 (admin/admin)" -ForegroundColor White
Write-Host "  • Prometheus:          http://localhost:9090" -ForegroundColor White
Write-Host "  • Jaeger Tracing:      http://localhost:16686" -ForegroundColor White
Write-Host ""
Write-Host "🧪 To test the setup:" -ForegroundColor Cyan
Write-Host "  python test_phase5.py" -ForegroundColor White
Write-Host ""
Write-Host "📈 To generate traffic:" -ForegroundColor Cyan
Write-Host "  python simulate_traffic.py" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop all services:" -ForegroundColor Cyan
Write-Host "  docker-compose down" -ForegroundColor White
