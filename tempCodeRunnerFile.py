@app.route('/analyze_stock', methods=['POST'])
@login_required
def analyze_stock():
    
    user_id = session['user_id']
    selected_symbol = request.form.get('stock_symbol')
    from_date_str = request.form.get('from_date')
    to_date_str = request.form.get('to_date')
    
    stock_message = None
    chart_data = None
    
    # Find the stock name corresponding to the selected symbol
    try:
        stock_index = COMPANIES.index(selected_symbol)
        stock_name = COMPANY_NAMES[stock_index]
    except ValueError:
        stock_message = "❗ Invalid stock symbol selected."
        return jsonify(message=stock_message, chart_data=None)

    try:
       
        recognizer = StockChangeRecognizer(stock_name, selected_symbol, from_date_str, to_date_str)
        
       
        recognizer.get_data_and_analyze()
        
    
        stock_message = recognizer.get_message()
        chart_data = recognizer.chart_data 

      
        user_settings = {}
        try:
            settings_doc = db.collection(f'artifacts/{app_id}/users/{user_id}/preferences').document('settings').get()
            if settings_doc.exists:
                user_settings = settings_doc.to_dict()
        except Exception as e:
            print(f"Error fetching user settings for email alert: {e}")

        email_alerts_enabled = user_settings.get('email_alerts_enabled', False)
        alert_email = user_settings.get('alert_email', '')
        email_password = user_settings.get('email_password', '')

        
        if email_alerts_enabled and alert_email and email_password and recognizer.big_delta:
            try:
                
                alert_dict = {selected_symbol: stock_message}
                mailer = SendEmail(alert_dict)
                mailer.send_mails(alert_email, alert_email, email_password) 
            except Exception as mail_e:
                stock_message += f"\n❌ Failed to send email alert: {mail_e}"
                print(f"Email sending error: {mail_e}")

    except Exception as e:
        stock_message = f"❌ An unexpected error occurred during analysis: {str(e)}"

   
    return jsonify(message=stock_message, chart_data=chart_data, stock_name=stock_name, symbol=selected_symbol)