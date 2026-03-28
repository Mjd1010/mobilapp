import flet as ft

# --- Part 1: Your Original Logic ---
user_profiles = {
    "+96890000001": {"avg_calls_per_hour": 3, "usual_country": "OM"},
    "+971501234567": {"avg_calls_per_hour": 5, "usual_country": "AE"},
    "+91990000002": {"avg_calls_per_hour": 4, "usual_country": "IN"}
}

def analyze_call_logic(number, calls, country):
    reasons = []
    user_profile = user_profiles.get(number)
    if user_profile:
        if int(calls) > user_profile["avg_calls_per_hour"] * 5:
            reasons.append("Sudden spike")
        if country.upper() != user_profile["usual_country"]:
            reasons.append("Unusual country")
    
    if len(reasons) == 0: return "ALLOW", "None", ft.colors.GREEN
    elif len(reasons) == 1: return "WARNING", reasons[0], ft.colors.AMBER
    else: return "REPORT", "High Risk", ft.colors.RED

# --- Part 2: Flet UI Interface ---

def main(page: ft.Page):
    page.title = "AI Call Security Monitor"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.scroll = "auto"

    # Input Fields
    num_input = ft.TextField(label="Phone Number", prefix_icon=ft.icons.PHONE, expand=True)
    calls_input = ft.TextField(label="Calls/Hour", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    country_input = ft.TextField(label="Country (OM, AE)", expand=True)

    # Data Table to show results
    results_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Number")),
            ft.DataColumn(ft.Text("Decision")),
            ft.DataColumn(ft.Text("Reason")),
        ],
        rows=[],
    )

    def analyze_clicked(e):
        if not num_input.value or not calls_input.value or not country_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("Please fill all fields!"))
            page.snack_bar.open = True
            page.update()
            return

        decision, reason, res_color = analyze_call_logic(
            num_input.value, calls_input.value, country_input.value
        )

        # Add new row to the table
        results_table.rows.insert(0, ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(num_input.value)),
                ft.DataCell(ft.Text(decision, color=res_color, weight="bold")),
                ft.DataCell(ft.Text(reason)),
            ]
        ))
        
        # Clear inputs and update
        num_input.value = ""
        calls_input.value = ""
        country_input.value = ""
        page.update()

    # Layout Assembly
    page.add(
        ft.Text("AI Call Security System", size=30, weight="bold", color=ft.colors.BLUE_200),
        ft.Row([num_input, calls_input, country_input]),
        ft.ElevatedButton(
            "Analyze Call", 
            icon=ft.icons.SECURITY, 
            on_click=analyze_clicked,
            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10))
        ),
        ft.Divider(),
        ft.Text("Recent Scan History", size=20, weight="w500"),
        results_table
    )

# To run in Pydroid 3 or PC
if __name__ == "__main__":
    ft.app(target=main)
