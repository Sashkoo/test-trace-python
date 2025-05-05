# test-trace.py
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
import time

# Настройка ресурса
resource = Resource(attributes={
    SERVICE_NAME: "test-service"
})

# Настройка трейсера
tracer_provider = TracerProvider(resource=resource)
trace.set_tracer_provider(tracer_provider)

# Экспортер в OpenTelemetry Collector
otlp_exporter = OTLPSpanExporter(
    endpoint="otel-collector.observability:4317",
    insecure=True
)

# Добавление экспортера к трейсеру
span_processor = BatchSpanProcessor(otlp_exporter)
tracer_provider.add_span_processor(span_processor)

# Получение трейсера
tracer = trace.get_tracer(__name__)

# Создание нескольких трейсов
for i in range(5):
    with tracer.start_as_current_span(f"test-span-{i}"):
        print(f"Doing work {i}")
        time.sleep(1)
        
        # Вложенный спан
        with tracer.start_as_current_span(f"sub-operation-{i}"):
            print(f"Doing sub-operation {i}")
            time.sleep(0.5)

# Ожидание отправки трейсов
time.sleep(5)
print("Test completed!")
