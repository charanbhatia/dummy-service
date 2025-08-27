# FastAPI Observability Stack

A complete observability solution for FastAPI applications with metrics, logging, and distributed tracing.

## 🚀 Features

- **Metrics Collection**: Prometheus integration with custom business metrics
- **Centralized Logging**: Structured logging with Loki and Promtail
- **Distributed Tracing**: Request tracing with Jaeger
- **Visualization**: Pre-configured Grafana dashboards
- **Containerized**: Full Docker Compose orchestration

## 📊 Stack Components

| Component | Purpose | Port |
|-----------|---------|------|
| FastAPI | Main application | 8000 |
| Prometheus | Metrics collection | 9090 |
| Grafana | Visualization & dashboards | 3000 |
| Loki | Log aggregation | 3100 |
| Promtail | Log shipping | - |
| Jaeger | Distributed tracing | 16686 |

## 🏃 Quick Start

1. **Clone and start the stack:**
   ```bash
   git clone https://github.com/charanbhatia/dummy-service
   cd dummy-service
   docker compose up -d
   ```

2. **Generate sample traffic:**
   ```bash
   python tests/simulate_traffic.py
   ```

3. **Access the applications:**
   - **FastAPI**: http://localhost:8000
   - **Grafana**: http://localhost:3000 (admin/admin)
   - **Prometheus**: http://localhost:9090
   - **Jaeger**: http://localhost:16686

## 📈 Dashboard Features

The pre-configured Grafana dashboard provides:

- **Request Rate**: Real-time HTTP request metrics
- **Response Times**: Latency tracking by endpoint
- **Error Rates**: HTTP status code breakdown
- **Active Users**: Current user session tracking
- **System Health**: Application performance metrics

## 🔧 Configuration

### Environment Variables

The application supports these environment variables:

- `LOG_LEVEL`: Logging level (default: INFO)
- `JAEGER_ENDPOINT`: Jaeger collector endpoint
- `PROMETHEUS_METRICS`: Enable/disable metrics (default: true)

### Custom Metrics

Add custom business metrics to `app/main.py`:

```python
from prometheus_client import Counter, Histogram

# Custom counter
user_registrations = Counter('user_registrations_total', 'Total user registrations')

# Custom histogram  
request_duration = Histogram('request_duration_seconds', 'Request duration')
```

## 🧪 Testing

Run the traffic simulator to generate realistic test data:

```bash
python tests/simulate_traffic.py
```

This creates:
- Normal user traffic patterns
- Error scenarios (404s, 500s)
- Slow endpoint testing
- Load testing bursts

## 📁 Project Structure

```
├── app/                    # FastAPI application
│   ├── main.py            # Main application
│   ├── models.py          # Data models
│   ├── logging_config.py  # Logging setup
│   └── tracing_config.py  # Tracing setup
├── grafana/               # Grafana configuration
│   ├── dashboards/        # Dashboard definitions
│   └── provisioning/      # Data sources & dashboards
├── loki/                  # Loki configuration
├── promtail/              # Promtail configuration
├── tests/                 # Test utilities
├── docker-compose.yml     # Service orchestration
├── prometheus.yml         # Prometheus configuration
└── requirements.txt       # Python dependencies
```

## 🛠️ Development

### Adding New Endpoints

1. Add endpoint to `app/main.py`
2. Include appropriate logging and metrics
3. Update the dashboard if needed
4. Test with traffic simulator

### Monitoring Setup

The stack automatically configures:
- Prometheus scraping of FastAPI metrics
- Log forwarding to Loki
- Jaeger trace collection
- Grafana data source connections

## 📜 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## 📞 Support

For questions or issues, please open a GitHub issue with:
- Environment details
- Steps to reproduce
- Expected vs actual behavior
