from database import personal_data_collection, notes_collection

def get_values(_id):
    """
    Returns a default profile dictionary for a given user ID.

    Args:
        _id (str): The user ID.

    Returns:
        dict: A dictionary containing default profile values.
    """
    return {
        'id': _id,
        'general': {
            'name': "",
            "age": 30,
            'weight': 70.0,
            'height': 175.5,
            'activity_level': 'Moderately Active',
            'gender': 'Male'
        },
        'goals': ['Muscle Gain'],
        'nutrition': {
            'calories': 2500,
            'protein': 150,
            'carbs': 300,
            'fats': 70
        }
    }

def create_profile(_id):
    """
    Creates a new user profile in the database with default values.

    Args:
        _id (str): The user ID.

    Returns:
        tuple: The inserted profile's MongoDB _id and the profile dictionary.
    """
    values = get_values(_id)
    profile = personal_data_collection.insert_one(values)
    values['_id'] = profile.inserted_id  # Add MongoDB-generated _id to the profile dict
    return profile.inserted_id, values

def get_profile(_id):
    """
    Retrieves a user profile from the database by user ID.

    Args:
        _id (str): The user ID.

    Returns:
        tuple: The profile's MongoDB _id and the profile dictionary if found, else (None, None).
    """
    profile = personal_data_collection.find_one({"id": _id})
    if profile:
        return profile['_id'], profile
    return None, None

def get_notes(_id):
    """
    Retrieves all notes associated with a user ID.

    Args:
        _id (str): The user ID.

    Returns:
        list: A list of note documents for the user.
    """
    notes = list(notes_collection.find({"user_id": _id}))
    return notes

def delete_profile(_id):
    """
    Deletes a user profile from the database by MongoDB _id.

    Args:
        _id (ObjectId): The MongoDB _id of the profile to delete.

    Returns:
        None
    """
    personal_data_collection.delete_one({"_id": _id})