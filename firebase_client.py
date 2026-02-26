"""
Firebase Firestore client for persistent state management, strategy storage, 
and real-time data streaming.
"""
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
import traceback

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1 import Client as FirestoreClient
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.firestore_v1.collection import CollectionReference

from config import config
from utils.logger import get_logger

logger = get_logger(__name__)

class FirebaseClient:
    """Firebase Firestore client wrapper with error handling and type safety"""
    
    def __init__(self):
        """Initialize Firebase with error handling"""
        self.client: Optional[FirestoreClient] = None
        self.initialized = False
        self._initialize()
    
    def _initialize(self) -> None:
        """Initialize Firebase app and client with robust error handling"""
        try:
            # Check if Firebase app is already initialized
            if not firebase_admin._apps:
                # Create credentials from config
                cred_dict = {
                    "type": config.firebase.type,
                    "project_id": config.firebase.project_id,
                    "private_key_id": config.firebase.private_key_id,
                    "private_key": config.firebase.private_key,
                    "client_email": config.firebase.client_email,
                    "client_id": config.firebase.client_id,
                    "auth_uri": config.firebase.auth_uri,
                    "token_uri": config.firebase.token_uri,
                    "auth_provider_x509_cert_url": config.firebase.auth_provider_x509_cert_url,
                    "client_x509_cert_url": config.firebase.client_x509_cert_url,
                    "universe_domain": config.firebase.universe_domain
                }
                
                cred = credentials.Certificate(cred_dict)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase app initialized successfully")
            
            self.client = firestore.client()
            self.initialized = True
            logger.info("Firestore client initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Firebase: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    
    def get_collection(self, collection_name: str) -> CollectionReference:
        """Get Firestore collection with validation"""
        if not self.initialized or