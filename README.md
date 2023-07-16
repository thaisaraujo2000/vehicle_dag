# Analysis of Fuel Types in Motor Vehicles 🚗⛽

This repository contains a project that uses the [Apache Airflow](https://airflow.apache.org/) platform to process and analyze fuel data in motor vehicles. The data is collected from the [Vehicle Fuel Economy Data US](https://www.kaggle.com/datasets/rajkumarpandey02/vehicle-fuel-economy-data-us?resource=download) dataset available on Kaggle.

## 🎯 Project Objective

The aim of this project is to explore the different types of fuels used in various vehicle models over the years, and to understand the distribution of fuel types among car manufacturers.

## 🚀 How to run

1. Clone this repository to your local machine:

    ```bash
    git clone https://github.com/your_username/vehicle_dag.git
    ```

2. Navigate to the cloned repository folder:

    ```bash
    cd vehicle_dag
    ```

3. Follow the [official installation instructions](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) to install Apache Airflow on your local machine.

4. After installing Apache Airflow, navigate to the `dags` folder that was created during the installation process (located in the `AIRFLOW_HOME` directory that Airflow monitors by default).

5. Create a new folder named `datas` inside the `dags` folder.

6. Download the CSV file from [Kaggle Vehicle Fuel Economy Data US](https://www.kaggle.com/datasets/rajkumarpandey02/vehicle-fuel-economy-data-us?resource=download) and place it in the `datas` folder.

7. Copy the DAG file (`vehicles_dag.py`) to the `dags` folder.

8. In a terminal window, run Docker Compose to start Apache Airflow:

    ```bash
    docker-compose up
    ```

9. Access the Airflow user interface in your web browser at: `http://localhost:8080`. The default credentials are: user `airflow` and password `airflow`.

10. In the DAG code (`vehicles_dag.py`), you can set the `schedule_interval` and `start_date` to schedule automatic execution of the DAG according to the specified interval and start date. With these parameters set in the code, you can enable the DAG in the Airflow user interface for it to run automatically according to the schedule. However, if you wish to manually execute the DAG, you can do so via the Airflow user interface. Once logged in, you should see the DAG `vehicles_dag` listed. To manually execute it, click on it and then click the "Trigger Dag" button.

## 📈 Task Flow (DAG)

The DAG (Directed Acyclic Graph) of this project consists of the following tasks:

1. `load_data`: Loads data from the CSV file.
2. `perform_analysis`: Performs an analysis of the data, grouping them by year and fuel type, counting the amount of each type and replacing null values with zero.
3. `group_by_fuelType`: Groups the data by fuel type and counts the number of unique models for each type.
4. `group_by_manufacturer`: Groups the data by manufacturer and fuel type, counting the number of unique models for each combination and replacing null values with 'Unknown'.
5. `success_task`: Prints a success message when the data analysis is completed.

The task flow is illustrated below:

```
load_data
   ↓
[perform_analysis, group_by_fuelType, group_by_manufacturer]
   ↓
success_task
```

## 🛠️ Dependencies

- Apache Airflow
- Pandas

## ⚖️ License

This project is under the MIT license. See the [LICENSE](LICENSE) file for more details.
