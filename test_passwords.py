import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Test different common password variations
passwords_to_try = [
    'sujit12',
    'Sujit12', 
    'sujit23',
    'Sujit23',
    'nirmalsujit981',
    'nirmal123',
    'password123'
]

username = 'nirmalsujitwebhook'
cluster = 'cluster0.ddqbrkp.mongodb.net'

print("Testing different password combinations...")

for password in passwords_to_try:
    try:
        uri = f'mongodb+srv://{username}:{password}@{cluster}/?appName=Cluster0'
        print(f'Testing password: {password}')
        
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        
        print(f'✅ SUCCESS! Password "{password}" works!')
        print(f'Update your .env file with:')
        print(f'MONGODB_URI={uri}')
        break
        
    except Exception as e:
        print(f'❌ Failed with "{password}": {str(e)[:50]}...')
        
print('\nIf none worked, you need to:')
print('1. Check MongoDB Atlas for the correct password')
print('2. Or create a new database user with a known password')
