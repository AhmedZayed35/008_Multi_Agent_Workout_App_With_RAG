from database import personal_data_collection, notes_collection
from datetime import datetime, timezone

def update_personal_data(existing, update_type, **kwargs):
    """
    Updates a user's personal data in the database based on the specified update type.
    Args:
        existing (dict): The existing user data document, including the '_id' field.
        update_type (str): The type of data to update. If 'goals', updates the 'goals' field specifically.
                           Otherwise, updates the field named by `update_type` with the provided kwargs.
        **kwargs: Arbitrary keyword arguments containing the new data to update.
    Returns:
        dict: The updated user data dictionary.
    Side Effects:
        Updates the corresponding document in the `personal_data_collection` database collection.
    Notes:
        - If `update_type` is 'goals', expects a 'goals' key in kwargs (defaulting to an empty list if not provided).
        - For other update types, the entire kwargs dictionary is set as the value for the specified field.
        - Assumes `personal_data_collection` is a valid MongoDB collection object available in the scope.
    """
    if update_type == 'goals':
        existing['goals'] = kwargs.get('goals', [])
        update_field = {'goals': existing['goals']}
    else:
        existing[update_type] = kwargs
        update_field = {update_type: existing[update_type]}

    personal_data_collection.update_one(
        {"_id": existing['_id']},
        {"$set": update_field}
    )

    return existing

def add_note(note, profile_id):
    new_note = {
        'user_id': profile_id,
        'text': note,
        '$vectorize': note,
        'metadata': {
            'injested': datetime.now(timezone.utc)
        }
    }

    result = notes_collection.insert_one(new_note)
    new_note['_id'] = result.inserted_id
    return new_note

def delete_note(_id):
    return notes_collection.delete_one({"_id": _id})
    