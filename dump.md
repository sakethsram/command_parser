automation/
│
├── input/
│   ├── pre_update.txt
│   └── post_update.txt
│
├── phase_1_isolation/
│   └── command_segmenter.py
│
├── phase_2_parsed/
│   ├── pre_parsed.json
│   └── post_parsed.json
│
├── phase_3_refined/
│   ├── pre_refined.json
│   └── post_refined.json
│
├── phase_4_tabular/
│   └── comparison_table.json
│
├── phase_5_comparison/
│   └── comparison_result.json
│
├── phase_6_report/
│   └── pre_post_validation_report.xlsx
│
├── logic/
│   ├── mx80_parser_engine.py
│   ├── mx80_models.py
│   ├── comparision.py
│   └── network_config_comparator.py
│
├── requirements.txt
└── readme.md



pre check have 2 steps - show commands for each model  , login to the device run the show commands and store it
upgrade - complete backend , 5 10 mins 

post - 90% same as pre , 





akash - input 
network_automation_api/
│
├── .env
├── requirements.txt
├── README.md
│
├── input/
│   ├── J1/show_commands.txt
│   ├── J2/show_commands.txt
│   ├── J3/show_commands.txt
│   ├── C1/show_commands.txt
│   ├── C2/show_commands.txt
│   └── C3/show_commands.txt
│
├── reports/
│   └── Model_Upgrade_Report_YYYYMMDD_HHMMSS.xlsx
│
├── logs/
│   └── api.log
│
├── database/
│   └── device_data.db
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routers/
 
│   │   └── dependencies.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── domain/
│   │   ├── devices/
│   │   │   ├── base_adapter.py
│   │   │   ├── juniper_adapter.py
│   │   │   └── cisco_adapter.py
│   │   │
│   │   ├── parsers/
│   │   │   ├── base_parser.py
│   │   │   ├── juniper_parser.py
│   │   │   └── cisco_parser.py
│   │   │
│   │   ├── commands/
│   │   │   └── command_loader.py
│   │   │
│   │   └── models/
│   │       └── parsed_data.py
│   │
│   ├── services/
│   │   ├── automation_service.py
│   │   └── report_service.py
│   │
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── base_repository.py
│   │   │   ├── sqlite_repository.py
│   │   │   └── schemas.sql
│   │   │
│   │   ├── filesystem/
│   │   │   ├── command_reader.py
│   │   │   └── report_writer.py
│   │   │
│   │   └── logging/
│   │       └── logger.py
│   │
│   ├── utils/
│   │   ├── timestamp.py
│   │   └── validators.py
│   │
│   └── tests/
│       ├── api/
│       ├── services/
│       └── domain/
│
└── docker/
    ├── Dockerfile
    └── docker-compose.yml