pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                script {
                    echo 'Checking out code...'
                    git branch: 'main',
                        url: 'https://github.com/Rechpa/fastAPITest.git'
                    echo 'Checkout completed.'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker Image...'
                    sh 'docker build -t fastapi-postgres-crud:5 .'
                }
            }
        }
    }

    post {
        success {
            echo 'Docker build completed successfully!'
        }
        failure {
            echo 'Docker build failed!'
        }
    }
}
