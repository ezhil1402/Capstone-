import pandas as pd

class Student:
    def __init__(self, name):
        self.name = name

class StudySession:
    def __init__(self, subject, hours, break_time):
        self.subject = subject
        self.hours = hours
        self.break_time = break_time

class ScheduleManager:
    def __init__(self):
        self.sessions = []

    def add_session(self, session):
        self.sessions.append(session)

    def total_study_hours(self):
        return sum(s.hours for s in self.sessions)

    def total_break_time(self):
        return sum(s.break_time for s in self.sessions)

class BurnoutAnalyzer:
    def analyze(self, total_hours, total_break):
        if total_hours > 8 and total_break < 1:
            return "High Burnout Risk"
        elif total_hours > 5:
            return "Moderate Risk"
        else:
            return "Low Risk"

class RecommendationEngine:
    def suggest(self, risk):
        if risk == "High Burnout Risk":
            return "⚠️ Take longer breaks and reduce study hours."
        elif risk == "Moderate Risk":
            return "⚡ Maintain balance. Add short breaks."
        else:
            return "✅ Good job! Keep your routine consistent."