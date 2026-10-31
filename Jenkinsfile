pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checkout'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies'
                sh 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                echo 'Running application tests'
                sh 'python -m pytest -v'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image'
                sh 'docker build -t devops-cicd-app:latest .'
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully!'
        }

        failure {
            echo 'CI Pipeline failed. Check the console output.'
        }
    }
}