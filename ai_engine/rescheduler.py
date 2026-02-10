def reschedule(teacher_id, current_day, analysis, cur):
    # analysis: { topic: (score, status) }
    incomplete = [t for t, data in analysis.items() if data[1] != "Completed"]
    if incomplete:
        next_day = current_day + 1
        for topic in incomplete:
            cur.execute("INSERT INTO timetable (teacher_id, day, topic) VALUES (?,?,?)", (teacher_id, next_day, topic))