"""
These are the various objects, or "models" that the api uses. Each class
should be represented as a javascript object, with the parameters as keys.
Dates should be encoded in ISO 8601.
"""

from attr import dataclass


# todo should assigned to be an id?
# todo get person by user id

@dataclass
class Task:
    """
    Represents a task object. `status` must be either "Completed", "In-Progress",
    or "Not Started". `task_name` is a brief description of the task. `assigned_to`
    is the user_id of the user to who the task is assigned to.
    """

    task_id: str
    task_name: str
    description: str
    assigned_to: str
    creation_date: int
    completion_date: int
    tags: [str]
    status: str


@dataclass
class Permission:
    """
    Represents a set of rules regarding a certain resource.
    """
    resource_id: str
    can_read: bool
    can_write: bool
    can_delete: bool


@dataclass
class User:
    """
    Represents a registered user of the MakerSpace. Users are
    those who will be using the dashboard (not visitors).
    """
    user_id: str
    first_name: str
    last_name: str
    assigned_tasks: [Task]
    permissions: [Permission]


# todo fix this - no date visited and is_new?
@dataclass
class Visitor:
    """
    Represents a visitor to the MakerSpace. `visitor_information`
    includes first name, last name, and major.
    """
    visit_id: str
    visitor_information: dict
    date_visited: str
    is_new: bool


@dataclass()
class Request:
    """
    Represents a maintenance request to the MakerSpace. `request_id`
    is not passed in when creating requests.
    """
    requester_name: str
    description: str
    request_id: str


@dataclass()
class Machine:
    """
    Represents a machine. `machine_state` can be either "1" (Working) or
    "O" (Not Working).
    """
    machine_name: str
    machine_state: int