#!/bin/bash

echo "🚀 Starting FastAPI Observability Stack"
echo "========================================"

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! command -v docker &> /dev/null; then
    echo "❌ Docker or Docker Compose not found!"
    echo "Please install Docker and Docker Compose to run the full stack."
    exit 1
fi

echo "📦 Building and starting services..."

# Build and start all services
docker-compose up --build -d

echo "⏳ Waiting for services to start..."
sleep 30

# Check if services are running
echo "🔍 Checking service status..."

services=("app:8000" "prometheus:9090" "grafana:3000" "jaeger:16686" "loki:3100")

for service in "${services[@]}"; do
    IFS=':' read -r name port <<< "$service"
    if curl -s "http://localhost:$port" > /dev/null; then
        echo "✅ $name running on port $port"
    else
        echo "❌ $name not responding on port $port"
    fi
done

echo ""
echo "🎉 Stack started successfully!"
echo ""
echo "📊 Access your services:"
echo "  • FastAPI Application: http://localhost:8000"
echo "  • Grafana Dashboard:   http://localhost:3000 (admin/admin)"
echo "  • Prometheus:          http://localhost:9090"
echo "  • Jaeger Tracing:      http://localhost:16686"
echo ""
echo "🧪 To test the setup:"
echo "  python test_phase5.py"
echo ""
echo "📈 To generate traffic:"
echo "  python simulate_traffic.py"
echo ""
echo "🛑 To stop all services:"
echo "  docker-compose down"
