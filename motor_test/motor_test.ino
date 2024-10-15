// Define pins:
#define FRONT_ENABLE_PIN_A 2
#define FRONT_ENABLE_PIN_B 3
#define L298N_1_IN1_PIN 5
#define L298N_1_IN2_PIN 6
#define L298N_1_IN3_PIN 7
#define L298N_1_IN4_PIN 8
#define BAUD_RATE 9600

enum motor_state 
{
  GO,
  STOP
};

void motor_controller_setup()
{
  // for the first motor controller (front two motors)
  pinMode(FRONT_ENABLE_PIN_A, OUTPUT);
  pinMode(FRONT_ENABLE_PIN_B, OUTPUT);
  pinMode(L298N_1_IN1_PIN, OUTPUT);
  pinMode(L298N_1_IN2_PIN, OUTPUT);
  pinMode(L298N_1_IN3_PIN, OUTPUT);
  pinMode(L298N_1_IN4_PIN, OUTPUT);

  // Turn off motors - Initial state
  digitalWrite(L298N_1_IN1_PIN, LOW);
  digitalWrite(L298N_1_IN2_PIN, LOW);
  digitalWrite(L298N_1_IN3_PIN, LOW);
  digitalWrite(L298N_1_IN4_PIN, LOW);
}

void motor_function(enum motor_state function)
{
  analogWrite(FRONT_ENABLE_PIN_A, 255);
  analogWrite(FRONT_ENABLE_PIN_B, 255);
  
  switch (function)
  {
    case GO: // forward
      digitalWrite(L298N_1_IN1_PIN, HIGH);
      digitalWrite(L298N_1_IN2_PIN, LOW);
      digitalWrite(L298N_1_IN3_PIN, HIGH);
      digitalWrite(L298N_1_IN4_PIN, LOW);
      break;
    case STOP: // stop
      digitalWrite(L298N_1_IN1_PIN, LOW);
      digitalWrite(L298N_1_IN2_PIN, LOW);
      digitalWrite(L298N_1_IN3_PIN, LOW);
      digitalWrite(L298N_1_IN4_PIN, LOW);
      break;
    default: // stop
      digitalWrite(L298N_1_IN1_PIN, LOW);
      digitalWrite(L298N_1_IN2_PIN, LOW);
      digitalWrite(L298N_1_IN3_PIN, LOW);
      digitalWrite(L298N_1_IN4_PIN, LOW);
      break;
  }
}

void full_stop()
{
  motor_function(STOP);
}

void go()
{
  motor_function(GO);
}

void setup() {
  // put your setup code here, to run once:
  
  // setup L298N H-bridge motor controller pins
  motor_controller_setup();
  
  //Begin Serial communication at a baudrate of 9600:
  Serial.begin(BAUD_RATE);
}

void loop() {
  // put your main code here, to run repeatedly:
  go();
  Serial.println("Spinning motor");
  delay(15000);
  Serial.println("Stopping motor");
  full_stop();
  delay(2000);
}
