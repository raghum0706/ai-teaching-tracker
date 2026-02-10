def generate_timetable(topics):
    # Sets 2 topics per day
    return { (i//2)+1: topics[i:i+2] for i in range(0, len(topics), 2) }