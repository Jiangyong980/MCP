"""Pydantic models for Zentao API data"""
from typing import List, Optional, Any, Dict
from pydantic import BaseModel
from datetime import datetime


# ==================== Common Models ====================

class User(BaseModel):
    """User model"""
    id: int
    account: str
    avatar: Optional[str] = None
    realname: Optional[str] = None


class PageInfo(BaseModel):
    """Pagination info"""
    page: int
    total: int
    limit: int


# ==================== Program Models ====================

class Program(BaseModel):
    """Program (项目集) model"""
    id: int
    name: str
    budget: Optional[int] = None
    budgetUnit: Optional[str] = None
    begin: Optional[str] = None
    end: Optional[str] = None
    realBegan: Optional[str] = None
    realEnd: Optional[str] = None
    parent: int = 0
    status: Optional[str] = None
    PM: Optional[User] = None
    progress: Optional[int] = None


class ProgramList(BaseModel):
    """Program list response"""
    programs: List[Program]


# ==================== Product Models ====================

class Product(BaseModel):
    """Product model"""
    id: int
    name: str
    code: Optional[str] = None
    program: Optional[int] = None
    line: Optional[int] = None
    type: Optional[str] = None  # normal, branch, platform
    status: Optional[str] = None  # normal, closed
    PO: Optional[User] = None
    QD: Optional[User] = None
    RD: Optional[User] = None
    desc: Optional[str] = None
    acl: Optional[str] = None  # open, private
    createdBy: Optional[User] = None
    createdDate: Optional[str] = None


class ProductList(BaseModel):
    """Product list response"""
    total: int
    products: List[Product]


# ==================== Project Models ====================

class Project(BaseModel):
    """Project model"""
    id: int
    name: str
    code: Optional[str] = None
    model: Optional[str] = None  # scrum, waterfall
    budget: Optional[int] = None
    budgetUnit: Optional[str] = None
    parent: Optional[int] = None
    begin: Optional[str] = None
    end: Optional[str] = None
    realBegan: Optional[str] = None
    realEnd: Optional[str] = None
    status: Optional[str] = None  # wait, doing, suspend, closed
    PM: Optional[str] = None
    progress: Optional[int] = None
    openedBy: Optional[str] = None
    openedDate: Optional[str] = None


class ProjectList(BaseModel):
    """Project list response"""
    page: int
    total: int
    limit: int
    projects: List[Project]


# ==================== Execution Models ====================

class Execution(BaseModel):
    """Execution (迭代/执行) model"""
    id: int
    name: str
    code: Optional[str] = None
    project: Optional[int] = None
    type: Optional[str] = None  # sprint, stage
    begin: Optional[str] = None
    end: Optional[str] = None
    status: Optional[str] = None
    PM: Optional[str] = None
    progress: Optional[int] = None
    openedBy: Optional[str] = None
    openedDate: Optional[str] = None


class ExecutionList(BaseModel):
    """Execution list response"""
    page: int
    total: int
    limit: int
    executions: List[Execution]


# ==================== Story Models ====================

class Story(BaseModel):
    """Story (需求) model"""
    id: int
    title: str
    product: Optional[int] = None
    branch: Optional[int] = None
    module: Optional[int] = None
    source: Optional[str] = None  # customer, user, po, market
    sourceNote: Optional[str] = None
    category: Optional[str] = None  # feature, interface, performance, safe, experience, improve, other
    stage: Optional[str] = None  # wait, planned, projected, developing, developed, testing, tested, verified, released, closed
    pri: Optional[int] = None
    estimate: Optional[float] = None
    verify: Optional[str] = None
    status: Optional[str] = None  # draft, active, closed, changed
    openedBy: Optional[User] = None
    openedDate: Optional[str] = None


class StoryList(BaseModel):
    """Story list response"""
    page: int
    total: int
    limit: int
    stories: List[Story]


# ==================== Task Models ====================

class Task(BaseModel):
    """Task model"""
    id: int
    name: str
    project: Optional[int] = None
    execution: Optional[int] = None
    module: Optional[int] = None
    story: Optional[int] = None
    type: Optional[str] = None  # design, devel, request, test, study, discuss, ui, affair, misc
    pri: Optional[int] = None
    estimate: Optional[float] = None
    consumed: Optional[float] = None
    left: Optional[float] = None
    deadline: Optional[str] = None
    status: Optional[str] = None  # wait, doing, done, closed, cancel
    desc: Optional[str] = None
    openedBy: Optional[User] = None
    openedDate: Optional[str] = None
    assignedTo: Optional[User] = None


class TaskList(BaseModel):
    """Task list response"""
    page: int
    total: int
    limit: int
    tasks: List[Task]


# ==================== Bug Models ====================

class Bug(BaseModel):
    """Bug model"""
    id: int
    title: str
    product: Optional[int] = None
    module: Optional[int] = None
    project: Optional[int] = None
    execution: Optional[int] = None
    severity: Optional[int] = None
    priority: Optional[int] = None
    status: Optional[str] = None  # active, resolved, closed
    confirmed: Optional[int] = None
    steps: Optional[str] = None
    openedBy: Optional[User] = None
    openedDate: Optional[str] = None


class BugList(BaseModel):
    """Bug list response"""
    page: int
    total: int
    limit: int
    bugs: List[Bug]
