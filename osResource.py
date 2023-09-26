
import os

# Get environment variables
azure_id = os.environ.get("AZURE_SUBSCRIPTION_ID")
kaggle_username = os.environ.get("KAGGLE_USERNAME")
kaggle_key = os.environ.get("KAGGLE_KEY")

# Print environment variables
print("User Environment variables:", azure_id, \
      kaggle_username, \
        kaggle_key)


