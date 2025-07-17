import logging
import os
from flask import Flask, request, jsonify, send_file, Response
from LabelPrinting_Backend import initialize, process_ticket
from production_config import ProductionConfig
from datetime import datetime

def setup_logging(app):
    log_dir = os.path.join(app.config['BASE_DIR'], 'logs')
    os.makedirs(log_dir, exist_ok=True)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # File handler for print requests
    file_handler = logging.FileHandler(
        os.path.join(log_dir, 'print_requests.log'),
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # Create logger
    logger = logging.getLogger('print_requests')
    logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    
    return logger

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)

    # Setup logging
    print_logger = setup_logging(app)

    # Validate configuration on startup
    try:
        ProductionConfig.validate_config()
    except ValueError as e:
        print(f"Configuration error: {e}")
        raise

    # Initialize once with config
    baseUrl, headers, baseDir = initialize(app.config)

    @app.route('/print_label', methods=['POST'])
    def print_label_api():
        data = request.get_json()
        ticketId = data.get('ticketId')
        laptop = data.get('laptop', False)

        print_logger.info(f"Print request - Ticket: {ticketId}, Laptop: {laptop}, IP: {request.remote_addr}")

        if not ticketId:
            print_logger.warning(f"Print request failed - No ticket ID provided, IP: {request.remote_addr}")
            return jsonify({'success': False, 'message': 'ticketId is required'}), 400

        try:
            success, message = process_ticket(baseUrl, headers, baseDir, ticketId, laptop)

            if success:
                print_logger.info(f"Print successful - Ticket: {ticketId}, Message: {message}")
            else:
                print_logger.error(f"Print failed - Ticket: {ticketId}, Message: {message}")
            
            return jsonify(message)
        except Exception as e:
            print_logger.error(f"Print error - Ticket: {ticketId}, Error: {str(e)}")
            return jsonify({'success': False, 'message': 'Internal server error'}), 500
    
    @app.route('/health')
    def health_check():
        return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})
    
    @app.route('/logs')
    def get_logs():
        """Download logs"""
        log_path = os.path.join(app.config['BASE_DIR'], 'logs', 'print_requests.log')

        if not os.path.exists(log_path):
            return jsonify({'error': 'Log file not found'}), 404
        
        return send_file(log_path, as_attachment=True, download_name='print_requests.log')
    
    @app.route('/logs/view')
    def view_logs():
        """View logs in browser"""
        log_path = os.path.join(app.config['BASE_DIR'], 'logs', 'print_requests.log')
        
        if not os.path.exists(log_path):
            return "Log file not found", 404
        
        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_content = f.read()
            
            # Return as plain text with proper formatting
            return Response(log_content, mimetype='text/plain')
        except Exception as e:
            return f"Error reading log file: {str(e)}", 500

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)