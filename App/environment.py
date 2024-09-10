import os


if os.getenv('IS_PRODUCTION') == 'TRUE':
    api_url = os.getenv('PRODUCTION_URL')
    IntegratorToken = ''
    IntegratorURL = ''
else:
    api_url = os.getenv('DEVELOPMENT_URL')
    IntegratorToken = os.getenv('INTEGRATOR_TOKEN')
    IntegratorURL = os.getenv('INTEGRATOR_URL')
    PassgageToken = os.getenv('PASSGAGE_TOKEN')
