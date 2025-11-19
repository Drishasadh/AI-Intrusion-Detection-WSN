# notifications.py - Secure communication and REAL SOUND notification system (Sound Only Output)
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time
import winsound  # ADDED FOR WINDOWS SYSTEM SOUNDS

class NotificationSystem:
    """Secure Communication & Sound Notification System"""
    
    def __init__(self):
        self.sms_log = []
        self.email_log = []
        self.alert_history = []
        self.config = None 
        
        # NEW: Map intrusion types to distinct Windows System Sound Aliases
        self.sound_map = {
            'vehicle': 'SystemHand',         # High severity sound
            'human': 'SystemExclamation',    # Medium severity sound
            'animal': 'SystemQuestion',      # Low severity sound
            'default': 'SystemAsterisk'
        }
        # Secure channel names for output realism (Used for internal logging only)
        self.radio_channel = "[SECURE DATALINK]"
        self.log_recipient = "command@border-cc.gov"
    
    def set_config(self, config):
        """Allows AIGateway to pass configuration details"""
        self.config = config
    
    def _play_sound(self, intrusion_type):
        """Play a type-specific default system sound for the alert (Windows only)"""
        
        sound_alias = self.sound_map.get(intrusion_type, 'SystemAsterisk')
        
        try:
            # THIS IS THE ONLY PRINT STATEMENT ALLOWED
            print(f"🔊 REAL SOUND ALERT: Playing Windows '{sound_alias}' for {intrusion_type.upper()}...")
            winsound.PlaySound(sound_alias, winsound.SND_ALIAS) 
            time.sleep(0.1) 
        except Exception as e:
            # Fallback for non-Windows systems or errors
            print(f"🔊 SIMULATED SOUND ALERT: Could not play real sound. Error: {e}")
            time.sleep(0.1)

    def send_sms_alert(self, message):
        """Simulate radio transmission/secure datalink (Executes Silently)"""
        timestamp = datetime.now()
        sms_data = {
            'timestamp': timestamp,
            'message': message,
            'recipient': self.radio_channel,
            'status': 'SENT'
        }
        self.sms_log.append(sms_data)
        # REMOVED: print(f"📻 RADIO TX SENT...") 
        return sms_data
    
    def send_email_alert(self, subject, message):
        """Simulate command center log update (Executes Silently)"""
        timestamp = datetime.now()
        email_data = {
            'timestamp': timestamp,
            'subject': subject,
            'message': message,
            'recipient': self.log_recipient,
            'status': 'SENT'
        }
        self.email_log.append(email_data)
        # REMOVED: print(f"💻 LOG MESSAGE SENT...") 
        return email_data
    
    def send_gsm_notification(self, intrusion_data):
        """Send comprehensive notification (Sound + Silent Logging)"""
        
        intrusion_type = intrusion_data['type'].lower()
        
        # 1. Play Intrusion-Specific Sound Alert (This is the only thing that prints)
        if self.config and self.config["notifications"]["sound_alerts"]:
             self._play_sound(intrusion_type)
        
        # 2. Prepare Message Body (used for silent logging)
        message_body = (f"INTRUSION ALERT: {intrusion_data['type'].upper()} detected "
                        f"at position {intrusion_data['position']}m. "
                        f"Confidence: {intrusion_data['confidence']:.2f}. "
                        f"Severity: {intrusion_data['severity']}")
        
        # 3. Send Radio/Datalink Transmission (Silent execution, logs data)
        self.send_sms_alert(message_body)
        
        # 4. Send Command Center Log Update (Silent execution, logs data)
        email_subject = f"Border Security Alert: {intrusion_data['type'].upper()} Intrusion"
        email_message = f"""
        BORDER SECURITY ALERT SYSTEM
        
        INTRUSION DETECTED
        
        Type: {intrusion_data['type'].upper()}
        Location: Position {intrusion_data['position']}m along border
        Confidence: {intrusion_data['confidence']:.2f}
        Severity Level: {intrusion_data['severity']}
        Time: {intrusion_data['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}
        
        Affected Nodes: {intrusion_data['affected_nodes']}
        Detection Range: {intrusion_data['detection_range']}m
        
        ACTION REQUIRED:
        - Dispatch response team
        - Verify with camera feeds
        - Monitor sensor network
        
        This is an automated alert from AI Border Security System.
        """
        
        self.send_email_alert(email_subject, email_message)
    
    def get_notification_stats(self):
        """Get notification statistics"""
        return {
            'total_sms': len(self.sms_log),
            'total_emails': len(self.email_log),
            'latest_sms': self.sms_log[-1] if self.sms_log else None,
            'latest_email': self.email_log[-1] if self.email_log else None
        }
