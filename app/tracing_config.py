import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


def setup_tracing(app):
    """Setup distributed tracing with OpenTelemetry and Jaeger"""
    
    # Create a resource with service information
    resource = Resource(attributes={
        SERVICE_NAME: "fastapi-observability-demo"
    })
    
    # Set up the tracer provider
    trace.set_tracer_provider(TracerProvider(resource=resource))
    tracer = trace.get_tracer(__name__)
    
    # Configure Jaeger exporter
    jaeger_exporter = JaegerExporter(
        agent_host_name=os.getenv("JAEGER_AGENT_HOST", "localhost"),
        agent_port=int(os.getenv("JAEGER_AGENT_PORT", "6831")),
    )
    
    # Create a BatchSpanProcessor and add the exporter to it
    span_processor = BatchSpanProcessor(jaeger_exporter)
    
    # Add the span processor to the tracer provider
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    # Instrument FastAPI
    FastAPIInstrumentor.instrument_app(app)
    
    return tracer


def get_tracer():
    """Get the tracer instance"""
    return trace.get_tracer(__name__)


def create_span(name: str, parent=None):
    """Create a new span"""
    tracer = get_tracer()
    return tracer.start_span(name, parent=parent)


def add_span_attributes(span, attributes: dict):
    """Add attributes to a span"""
    for key, value in attributes.items():
        span.set_attribute(key, value)


def add_span_event(span, name: str, attributes: dict = None):
    """Add an event to a span"""
    span.add_event(name, attributes or {})
