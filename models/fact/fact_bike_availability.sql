{{ config(
    materialized='incremental',
    unique_key=['station_id', 'recorded_at_minute'],
    incremental_strategy='delete+insert',
    on_schema_change='sync_all_columns'
) }}

with status as (
    select *
    from {{ ref('stg_station_status') }}
    {% if is_incremental() %}
    where recorded_at_minute > (select max(recorded_at_minute) from {{ this }})
    {% endif %}
)
select
    s.station_id,
    s.recorded_at_minute,
    s.bikes_available,
    s.docks_available,
    d.capacity,
    1.0 * s.bikes_available / nullif(d.capacity, 0) as availability_pct
from status s
left join {{ ref('dim_station') }} d using (station_id)