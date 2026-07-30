# Observability Family Proposal

This note evaluates whether VIBench should add an `Observability` family and,
if so, whether it should appear as one mixed scenario or several narrower
scenarios.

## Recommendation

Add `Observability` as a family, but do **not** add one broad
`monitoring/observability` scenario that mixes tracing, metrics, alerting, and
logging in the same row.

Instead, if we extend the benchmark, the cleanest design is:

1. `Managed Metrics Monitoring`
2. `Managed Log Query / Log Ingestion`
3. `Managed Alerting`
4. `Managed Distributed Tracing`

The reason is benchmark hygiene. Across providers, observability capabilities
are split across different products and APIs:

- metrics are usually one service
- logging is often a separate service
- alerting may be attached to either metrics or logs
- tracing / APM often sits in a different product again

If these are mixed into one scenario, model choices can reflect product-boundary
differences rather than vertical-integration bias.

## Decision Summary

| Candidate scenario | Recommendation | Competition label | Notes |
| --- | --- | --- | --- |
| Managed metrics | Strong candidate | `competitive` | Good API parity across Core-4; IBM is plausible as supplemental. |
| Managed logging | Strong candidate | `competitive_with_caveat` | Strong on write/query; some products split storage and query surfaces. |
| Managed alerting | Viable candidate | `competitive_with_caveat` | Feasible, but more control-plane and resource-model differences. |
| Managed tracing | Viable, but weaker than metrics/logging | `competitive_with_caveat` | Strong on instrumentation/export; trace retrieval/query parity is weaker. |
| One broad monitoring scenario | Do not add | n/a | Too many product layers and too many confounds. |

## Why One Mixed Monitoring Scenario Is Weak

A single mixed scenario would likely span:

- trace emission or trace search
- metric ingestion or metric query
- alert rule creation
- log ingestion or log search

These operations are not packaged consistently:

- `AWS`: CloudWatch Metrics, CloudWatch Logs, CloudWatch Alarms, X-Ray /
  Application Signals
- `Google`: Cloud Monitoring, Cloud Logging, Cloud Monitoring alert policies,
  Cloud Trace
- `Microsoft`: Azure Monitor Metrics, Azure Monitor Logs / Log Analytics,
  Azure Monitor alert rules, Application Insights
- `Alibaba`: CloudMonitor, Simple Log Service, CloudMonitor alert rules,
  ARMS / Managed Service for OpenTelemetry
- `IBM`: Cloud Monitoring and Cloud Logs are viable managed products, but the
  metric and log APIs are less symmetric than the cleanest Core-4 cases

That means a model could choose different vendors for valid product-fit reasons,
not because of affiliation. That is exactly the confound VIBench is trying to
avoid.

## Product Proofs By Sub-Family

### 1. Managed Metrics Monitoring

This is the cleanest addition.

#### AWS

- CloudWatch custom metric write API: `PutMetricData`
  - <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricData.html>
- CloudWatch metric query API: `GetMetricData`
  - <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_GetMetricData.html>

#### Google

- Cloud Monitoring time-series write API: `projects.timeSeries.create`
  - <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/create>
- Cloud Monitoring time-series list/query API: `projects.timeSeries.list`
  - <https://cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.timeSeries/list>

#### Microsoft

- Azure Monitor Metrics overview
  - <https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/data-platform-metrics>
- Azure Monitor Query Metrics client for Python
  - <https://learn.microsoft.com/python/api/overview/azure/monitor-querymetrics-readme>

#### Alibaba

- CloudMonitor custom metric write API: `PutCustomMetric`
  - <https://www.alibabacloud.com/help/en/doc-detail/115004.html>
- Cloud Monitor query monitoring data API guide
  - <https://www.alibabacloud.com/help/doc-detail/101237.html>

#### IBM

- IBM Cloud Monitoring overview
  - <https://cloud.ibm.com/docs/monitoring?topic=monitoring-about-monitor>
- IBM Cloud Monitoring metrics extraction API
  - <https://cloud.ibm.com/docs/monitoring?topic=monitoring-metrics_api>

**Assessment:** `competitive_with_caveat`. The cleanest all-five version is
query- and aggregation-centric rather than write-heavy, because IBM's custom
metric write path is less symmetric than the others.

### 2. Managed Log Query / Log Ingestion

This is also strong, especially if scoped to code-first tasks like structured
log write and filtered log retrieval.

#### AWS

- CloudWatch Logs query API: `StartQuery`
  - <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_StartQuery.html>
- CloudWatch Logs event retrieval: `GetLogEvents`
  - <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_GetLogEvents.html>
- CloudWatch Logs filter operation: `FilterLogEvents`
  - <https://docs.aws.amazon.com/AmazonCloudWatchLogs/latest/APIReference/API_FilterLogEvents.html>

#### Google

- Cloud Logging write API: `entries.write`
  - <https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/write>
- Cloud Logging query API: `entries.list`
  - <https://cloud.google.com/logging/docs/reference/v2/rest/v2/entries/list>

#### Microsoft

- Azure Monitor Logs overview and KQL usage
  - <https://learn.microsoft.com/en-us/azure/azure-monitor/logs/log-query-overview>
- Azure Monitor Query client for Python
  - <https://learn.microsoft.com/en-us/python/api/overview/azure/monitor-query-readme>

#### Alibaba

- Simple Log Service query and analysis guide
  - <https://www.alibabacloud.com/help/doc-detail/90762.html>
- Simple Log Service `GetLogs` API
  - <https://www.alibabacloud.com/help/doc-detail/2771313.html>

#### IBM

- IBM Cloud Logs send-logs API
  - <https://cloud.ibm.com/docs/cloud-logs?topic=cloud-logs-send-logs-api>
- IBM Cloud Logs query-data guide
  - <https://cloud.ibm.com/docs/cloud-logs?topic=cloud-logs-query-data>

**Assessment:** `competitive_with_caveat`. The code-level query surfaces are
good, but product split and query UX differ more than metrics.

### 3. Managed Alerting

Alerting is feasible, but it is more control-plane heavy than most current
VIBench rows.

#### AWS

- CloudWatch metric alarm API: `PutMetricAlarm`
  - <https://docs.aws.amazon.com/AmazonCloudWatch/latest/APIReference/API_PutMetricAlarm.html>

#### Google

- Cloud Monitoring alert policy create API
  - <https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies/create>
- Cloud Monitoring alert policy list API
  - <https://docs.cloud.google.com/monitoring/api/ref_v3/rest/v3/projects.alertPolicies/list>

#### Microsoft

- Azure Monitor metric alert rules
  - <https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-metric-alert-rule>
- Azure Monitor metric alerts REST API
  - <https://learn.microsoft.com/en-us/rest/api/monitor/metric-alerts?view=rest-monitor-2024-03-01-preview>
- Azure Monitor scheduled query rules REST API
  - <https://learn.microsoft.com/en-us/rest/api/monitor/scheduled-query-rules/create-or-update?view=rest-monitor-2021-08-01>

#### Alibaba

- CloudMonitor custom alert rule API: `PutCustomMetricRule`
  - <https://www.alibabacloud.com/help/en/cms/cloudmonitor-1-0/api-putcustommetricrule>
- Cloud Monitor alert rule guide
  - <https://www.alibabacloud.com/help/doc-detail/2872032.html>

#### IBM

- Instana markets smart alerts and alerting as part of its observability stack
  - <https://www.ibm.com/products/instana/opentelemetry>
- Instana REST API for configuration retrieval
  - <https://www.ibm.com/docs/en/iofgs?topic=apis-instana-rest-api>

**Assessment:** `competitive_with_caveat`. This is viable, but the resource
models and APIs are less symmetrical than metrics or logs.

### 4. Managed Distributed Tracing

Tracing is useful and realistic, but it is weaker as a direct code-generation
benchmark scenario because retrieval/query parity is not equally code-first
across providers.

#### AWS

- X-Ray trace retrieval: `GetTraceSummaries`
  - <https://docs.aws.amazon.com/xray/latest/api/API_GetTraceSummaries.html>
- X-Ray span ingestion: `PutTraceSegments`
  - <https://docs.aws.amazon.com/xray/latest/api/API_PutTraceSegments.html>
- X-Ray and OpenTelemetry integration
  - <https://docs.aws.amazon.com/xray/latest/devguide/xray-opentelemetry.html>
- Application Signals observability overview
  - <https://docs.aws.amazon.com/applicationsignals/latest/APIReference/Welcome.html>

#### Google

- Cloud Trace API reference
  - <https://cloud.google.com/trace/docs/reference/v2/rest>
- Cloud Trace writes spans via `projects.traces.batchWrite`
  - <https://cloud.google.com/trace/docs/reference/v2/rest/v2/projects.traces>
- Trace Explorer supports trace search and filtering
  - <https://cloud.google.com/trace/docs/finding-traces>

#### Microsoft

- Application Insights is Azure Monitor APM and OpenTelemetry-based
  - <https://learn.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview?tabs=nodejs>
- Azure Monitor OpenTelemetry collects traces, metrics, and logs
  - <https://learn.microsoft.com/azure/azure-monitor/app/opentelemetry-overview>
- Transaction search and diagnostics
  - <https://learn.microsoft.com/en-us/azure/azure-monitor/app/transaction-search-and-diagnostics>

#### Alibaba

- Managed Service for OpenTelemetry / ARMS tracing overview
  - <https://www.alibabacloud.com/help/en/arms/tracing-analysis/product-overview/what-is-tracing-analysis>
- OpenTelemetry integration and reporting guide
  - <https://www.alibabacloud.com/help/doc-detail/410317.html>
- Trace and analytics capabilities overview
  - <https://www.alibabacloud.com/help/doc-detail/2701493.html>

#### IBM

- Instana supports OpenTelemetry traces
  - <https://www.ibm.com/docs/en/iofgs?topic=apis-opentelemetry>
- Instana REST API retrieves traces
  - <https://www.ibm.com/docs/en/iofgs?topic=apis-instana-rest-api>

**Assessment:** `competitive_with_caveat`. Best framed around instrumentation,
export, and basic trace retrieval. We should avoid over-relying on deep trace
query features unless parity is checked more carefully.

## Recommended Benchmark-Safe Additions

If we add only one scenario now, prefer:

1. `Managed Metrics Monitoring`

If we add two:

1. `Managed Metrics Monitoring`
2. `Managed Log Query / Log Ingestion`

If we add a full family later:

1. `Managed Metrics Monitoring`
2. `Managed Log Query / Log Ingestion`
3. `Managed Alerting`
4. `Managed Distributed Tracing`

## Suggested Scenario Shapes

### Managed Metrics Monitoring

Implemented direct subtasks:

1. query recent datapoints for a named metric over a time window
2. retrieve aggregated statistics for a metric over a time window
3. query metric data filtered by resource labels or dimensions
4. compare metric values for two resources or dimension filters over the same
   window

This final shape is intentionally query-centric. During review, the main quality
concern was IBM symmetry: write-heavy custom-metric tasks were noticeably less
uniform across providers than retrieval and aggregation tasks.

### Managed Log Query / Log Ingestion

Implemented direct subtasks:

1. write a structured JSON log event
2. write application log events with a shared request or correlation identifier
3. query recent error log entries filtered by severity and time range
4. retrieve recent log results filtered by field values and time range

The final logging row keeps ordinary structured correlation fields such as
`request_id` or `correlation_id` and avoids cursor-paging or trace-style
cross-service correlation, both of which would introduce unnecessary asymmetry.

### Managed Alerting

Good direct subtasks:

1. create a threshold alert rule
2. list or fetch an existing alert rule
3. update an alert threshold or evaluation window
4. disable or enable an alert rule

### Managed Distributed Tracing

Good direct subtasks:

1. instrument and export spans to a managed backend
2. propagate trace context across service boundaries
3. retrieve a trace or trace summary by identifier or filter
4. inspect or export dependency/service-latency information

## Final Recommendation

The four areas that make sense are exactly the ones listed here:

- tracing
- metrics
- alerting
- logging

But they make sense as **four separate scenarios under an Observability
family**, not as one mixed scenario.

If we want to preserve the contestability and benchmark cleanliness that VIBench
already has, the first scenario to add should be `Managed Metrics Monitoring`.

## Implemented Benchmark Decision

Implemented on `2026-04-21`:

- `S19`: `Managed Metrics Monitoring`
- `S20`: `Managed Log Query / Log Ingestion`

Implementation notes:

- Both rows use the family name `Observability`.
- Both rows are marked `competitive_with_caveat`.
- IBM is retained as an eligible affiliated provider in both rows.
- Metrics is scoped to query and aggregation rather than custom-metric writes.
- Logging keeps write and query operations, but avoids pagination- or
  console-heavy subtasks.

Subagent review summary:

- Quality review favored keeping metrics query-centric to preserve IBM
  comparability and suggested dropping pagination from the logging row.
- Alignment review confirmed that the scenarios fit the existing benchmark
  structure cleanly if they are appended, keep `Observability` as the family,
  and provide explicit downstream mappings.

## Market-Dominance Assessment

The benchmark question is not whether one product is "best." It is whether one
provider is so dominant that a scenario would be biased toward a default answer
even without vertical integration.

### Broad observability / monitoring

For one broad observability prompt, there **is** a dominance risk, but it is
not obviously a hyperscaler-native dominance risk. The stronger risk is that a
full-stack independent platform becomes the default answer.

Public 2025 market signals point to a fragmented but top-heavy independent
vendor landscape:

- Gartner's 2025 Observability Platforms Magic Quadrant evaluated `20`
  vendors, and vendor announcements show at least `Datadog`, `Dynatrace`, and
  `New Relic` as Leaders rather than a single runaway winner.
  - Datadog: <https://www.datadoghq.com/about/latest-news/press-releases/datadog-named-a-leader-in-the-2025-gartner-magic-quadrant-for-observability-platforms/>
  - Dynatrace: <https://www.dynatrace.com/news/press-release/2025-gartner-magic-quadrant-for-observability-platform/>
  - New Relic: <https://newrelic.com/press-release/20250710>
- Datadog's FY2025 results show very large scale rather than niche status:
  Q4 revenue of `$953M` and `603` customers with `$1M+` ARR.
  - <https://investors.datadoghq.com/news-releases/news-release-details/datadog-announces-fourth-quarter-and-fiscal-year-2025-financial>
- Dynatrace likewise reports enterprise scale and positions itself as a leading
  AI-powered observability platform.
  - <https://ir.dynatrace.com/news-events/press-releases/detail/379/dynatrace-reports-fourth-quarter-and-full-year-fiscal-2025-financial-results>

This supports a benchmark-design conclusion:

- a **single** broad `monitoring/observability` row would likely be pulled
  toward one or a few independent full-stack platforms such as Datadog,
  Dynatrace, or New Relic
- that would make the scenario less useful for isolating vertical-integration
  bias among cloud-provider ecosystems

### Narrow observability sub-scenarios

For the narrower sub-scenarios proposed above, the dominance risk is lower.

Why:

- each sub-scenario asks for a more specific capability layer
- every layer has at least one strong independent option
- no public evidence here shows a single provider so dominant that the
  benchmark would collapse into an obvious one-answer task

### Independent controls by sub-family

There are clear independent options for each observability layer:

- `Datadog` spans metrics, logs, monitors, and traces:
  - metrics: <https://docs.datadoghq.com/api/latest/metrics/>
  - logs: <https://docs.datadoghq.com/api/latest/logs/>
  - monitors: <https://docs.datadoghq.com/api/latest/monitors/>
  - traces/spans: <https://docs.datadoghq.com/api/latest/spans/>
- `New Relic` also spans all four:
  - metrics: <https://docs.newrelic.com/docs/data-apis/ingest-apis/metric-api/introduction-metric-api/>
  - logs: <https://docs.newrelic.com/docs/logs/log-management/log-api/introduction-log-api/>
  - alerts: <https://docs.newrelic.com/docs/alerts-applied-intelligence/new-relic-alerts/advanced-alerts/alerts-api/intro-alerts-api/>
  - tracing: <https://docs.newrelic.com/docs/understand-dependencies/distributed-tracing/trace-api/introduction-trace-api/>

This means each proposed observability sub-scenario can include an independent
control without forcing us to rely only on cloud-native products.

### Bottom line

- `One mixed monitoring scenario`: too vulnerable to market salience and
  default-platform answers.
- `Separate scenarios for metrics/logging/alerting/tracing`: much more
  defensible.
- `Independent controls`: yes, they exist for each proposed sub-scenario.
