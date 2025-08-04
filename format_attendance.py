def format_attendance(raw_text):
    lines = raw_text.split("\n")
    formatted_lines = ["Attendance Report"]

    for line in lines:
        parts = line.split()
        if len(parts) >= 5 and parts[0].isdigit():
            subject = parts[1]
            percent = parts[-1]
            formatted_lines.append(f"{subject:<12} {percent}%")
        elif line.startswith("TOTAL"):
            percent = line.split()[-1]
            formatted_lines.append(f"\nTOTAL: {percent}%")

    return "\n".join(formatted_lines)
