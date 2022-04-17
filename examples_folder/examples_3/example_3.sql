create table example_3 as
select
     sql_views.id thing_id
     , sql_views.name
     , sql_views.sql
     , 'view' as tpe
from
    periscope_usage_data.sql_views
where
     sql_views.deleted_at is null
union all
select
    charts.id
    , charts.name
    , charts.sql
    , 'chart' as tpe
from
    periscope_usage_data.charts
join periscope_usage_data.dashboards on
    charts.dashboard_id = dashboards.id
where
    charts.deleted_at is null
    and dashboards.deleted_at is null
union all
select
    csvs.id
    , csvs.name
    , '' as sql
    , 'csv' as tpe
from
    periscope_usage_data.csv
