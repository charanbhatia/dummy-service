import os
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


def setup_tracing(app):
    """Setup distributed tracing with OpenTelemetry and Jaeger"""
    
    try:
        print("🔍 Initializing OpenTelemetry tracing...")
        
        # Create a resource with service information
        resource = Resource(attributes={
            SERVICE_NAME: "fastapi-observability-demo"
        })
        print(f"✅ Created resource with service name: fastapi-observability-demo")
        
        # Set up the tracer provider
        trace.set_tracer_provider(TracerProvider(resource=resource))
        tracer = trace.get_tracer(__name__)
        print("✅ Tracer provider initialized")
        
        # Configure OTLP exporter for Jaeger
        otlp_exporter = OTLPSpanExporter(
            endpoint=os.getenv("JAEGER_ENDPOINT", "http://jaeger:4317"),
            insecure=True,
        )
        print(f"✅ OTLP exporter configured for endpoint: {os.getenv('JAEGER_ENDPOINT', 'http://jaeger:4317')}")
        
        # Create a BatchSpanProcessor and add the exporter to it
        span_processor = BatchSpanProcessor(otlp_exporter)
        print("✅ Span processor created")
        
        # Add the span processor to the tracer provider
        trace.get_tracer_provider().add_span_processor(span_processor)
        print("✅ Span processor added to tracer provider")
        
        # Instrument FastAPI
        FastAPIInstrumentor.instrument_app(app)
        print("✅ FastAPI instrumented for tracing")
        
        print("🚀 OpenTelemetry tracing setup completed successfully!")
        return tracer
        
    except Exception as e:
        print(f"❌ Error setting up tracing: {e}")
        import traceback
        traceback.print_exc()
        return None


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
