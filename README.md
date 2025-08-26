# FastAPI Observability Demo

A comprehensive FastAPI application demonstrating complete observability with metrics, logging, and distributed tracing using modern monitoring tools.

## 🎯 Project Overview

This project showcases a production-ready observability stack for FastAPI applications, implementing the three pillars of observability:

- **📊 Metrics**: Real-time performance and business metrics with Prometheus
- **📝 Logs**: Structured logging with correlation IDs using Loki
- **🔍 Traces**: Distributed request tracing with Jaeger and OpenTelemetry

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   FastAPI App   │────│   Prometheus    │────│    Grafana      │
│   (Port 8000)   │    │   (Port 9090)   │    │   (Port 3000)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                                              │
         │              ┌─────────────────┐             │
         └──────────────│     Jaeger      │─────────────┘
         │              │   (Port 16686)  │             │
         │              └─────────────────┘             │
         │                                              │
         │              ┌─────────────────┐             │
         └──────────────│      Loki       │─────────────┘
                        │   (Port 3100)   │
                        └─────────────────┘
                                 │
                        ┌─────────────────┐
                        │    Promtail     │
                        │  (Log Shipper)  │
                        └─────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose
- Python 3.11+
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd fastapi-observability-demo
```

### 2. Start the Complete Stack

**Windows (PowerShell):**
```powershell
.\start_stack.ps1
```

**Linux/Mac:**
```bash
chmod +x start_stack.sh
./start_stack.sh
```

**Manual Docker Compose:**
```bash
docker-compose up --build -d
```

### 3. Generate Test Traffic

```bash
python tests/simulate_traffic.py
```

### 4. Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| **FastAPI Application** | http://localhost:8000 | - |
| **Grafana Dashboard** | http://localhost:3000 | admin/admin |
| **Prometheus** | http://localhost:9090 | - |
| **Jaeger Tracing** | http://localhost:16686 | - |

## 🎯 Features

### FastAPI Application
- RESTful API with CRUD operations for users
- Health check endpoints
- Error simulation endpoints
- Slow endpoint for latency testing
- Comprehensive input validation

### Observability Stack
- **Custom Metrics**: Request count, latency, error rates, active users
- **Structured Logging**: JSON logs with correlation IDs and context
- **Distributed Tracing**: Request flow visualization across services
- **Pre-built Dashboards**: Ready-to-use Grafana dashboards
- **Alerting Ready**: Prometheus metrics ready for alerting rules

## 📊 Monitoring Capabilities

### Metrics (Prometheus)
- `http_requests_total` - Total HTTP requests by method, endpoint, status
- `http_request_duration_seconds` - Request latency histogram
- `active_users_total` - Current number of users in system
- `http_errors_total` - Error count by type and endpoint
- Built-in FastAPI metrics via instrumentator

### Logs (Loki + Promtail)
- Structured JSON logging
- Request/response correlation
- Error tracking and context
- Performance monitoring
- Business logic events

### Traces (Jaeger + OpenTelemetry)
- End-to-end request tracing
- Span-level performance analysis
- Service dependency mapping
- Error propagation tracking

## 🧪 Testing

### Run All Tests
```bash
python tests/test_phase5.py
```

### Specific Test Scenarios
```bash
# Test logging functionality
python tests/test_logging.py

# Test Prometheus metrics
python tests/test_phase2.py

# Test distributed tracing
python tests/test_tracing.py

# Generate realistic traffic
python tests/simulate_traffic.py
```

## 📈 API Endpoints

### Core Endpoints
- `GET /` - Root endpoint with timestamp
- `GET /health` - Health check with system status
- `GET /metrics` - Prometheus metrics endpoint
- `GET /metrics-info` - Information about available metrics

### User Management
- `GET /users` - List all users
- `POST /users` - Create a new user
- `GET /users/{id}` - Get user by ID
- `DELETE /users/{id}` - Delete user by ID

### Testing Endpoints
- `GET /slow` - Simulates slow processing (2-5 seconds)
- `GET /error` - Always returns 500 error for testing

## 🔧 Configuration

### Environment Variables
- `JAEGER_AGENT_HOST` - Jaeger agent hostname
- `JAEGER_AGENT_PORT` - Jaeger agent port
- `PYTHONUNBUFFERED` - Python output buffering

### Docker Compose Services
- **app**: FastAPI application
- **prometheus**: Metrics collection
- **grafana**: Dashboards and visualization
- **jaeger**: Distributed tracing
- **loki**: Log aggregation
- **promtail**: Log shipping

## 📁 Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application with observability
│   ├── models.py            # Pydantic models
│   ├── logging_config.py    # Structured logging configuration
│   └── tracing_config.py    # OpenTelemetry tracing setup
├── grafana/
│   ├── dashboards/          # Pre-built Grafana dashboards
│   └── provisioning/        # Datasource and dashboard configs
├── tests/
│   ├── test_phase2.py       # Prometheus metrics tests
│   ├── test_logging.py      # Logging functionality tests
│   ├── test_tracing.py      # Distributed tracing tests
│   ├── test_phase5.py       # Complete stack integration tests
│   └── simulate_traffic.py  # Traffic generation for testing
├── loki/
│   └── loki-config.yml      # Loki configuration
├── promtail/
│   └── promtail-config.yml  # Log shipping configuration
├── docker-compose.yml       # Complete stack definition
├── Dockerfile              # FastAPI app container
├── prometheus.yml           # Prometheus scrape configuration
├── requirements.txt         # Python dependencies
├── start_stack.ps1         # Windows startup script
└── start_stack.sh          # Linux/Mac startup script
```

## 🎬 Demo Script for Recording

### 1. Start the Stack (30 seconds)
```bash
.\start_stack.ps1
# Show services starting up
docker-compose ps
```

### 2. Generate Traffic (1 minute)
```bash
python tests/simulate_traffic.py
# Show real-time requests in terminal
```

### 3. Grafana Dashboard (2 minutes)
- Open http://localhost:3000 (admin/admin)
- Navigate to FastAPI Observability Dashboard
- Show real-time metrics, logs, and traces
- Demonstrate filtering and time ranges

### 4. Prometheus Metrics (30 seconds)
- Open http://localhost:9090
- Query custom metrics: `http_requests_total`
- Show metric exploration

### 5. Jaeger Traces (1 minute)
- Open http://localhost:16686
- Search for traces from fastapi-observability-demo
- Show trace details and spans

## 🛑 Cleanup

Stop all services:
```bash
docker-compose down
```

Remove all data volumes:
```bash
docker-compose down -v
```

## 🎯 Project Phases

This project was built incrementally across multiple phases:

1. **Phase 1** (branch: `main`): Basic FastAPI service setup
2. **Phase 2** (branch: `prometheus-metrics`): Prometheus metrics integration
3. **Phase 3** (branch: `logging`): Structured logging implementation
4. **Phase 4** (branch: `tracing`): Distributed tracing with OpenTelemetry
5. **Phase 5** (branch: `grafana`): Complete observability stack with Grafana

Each phase is available as a separate Git branch for learning and reference.

## 🔍 Key Learning Points

- **Observability Strategy**: Implementing comprehensive monitoring from day one
- **Modern Tooling**: Using industry-standard observability tools
- **Production Readiness**: Configuration suitable for production environments
- **Developer Experience**: Easy local development and testing workflow
- **Performance Monitoring**: Real-time insights into application behavior

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is for educational and demonstration purposes.

## 🙏 Acknowledgments

- FastAPI framework and community
- Prometheus and Grafana projects
- OpenTelemetry community
- Docker and containerization ecosystem
