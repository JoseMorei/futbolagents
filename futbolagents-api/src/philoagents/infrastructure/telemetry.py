from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from loguru import logger

from philoagents.config import settings


def configure_telemetry(app) -> None:
    if not settings.OTEL_ENABLED:
        logger.warning(
            "OpenTelemetry tracing is disabled. Set OTEL_ENABLED=true to enable."
        )
        return

    provider = TracerProvider()
    exporter = OTLPSpanExporter(endpoint=settings.JAEGER_ENDPOINT, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument_app(app)

    logger.info(
        f"OpenTelemetry configured. Sending traces to Jaeger at {settings.JAEGER_ENDPOINT}"
    )
