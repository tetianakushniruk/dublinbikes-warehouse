{% snapshot snap_station_status %}
{%- set src -%}{{ ref('stg_station_status') }}{%- endset %}
{{ config(
    unique_key='station_id',
    strategy='check',
    check_cols=['bikes_available', 'docks_available']
) }}
select * from {{ src }}
{% endsnapshot %}