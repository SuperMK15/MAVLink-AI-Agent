from modules import (
    speech,
    llm,
    drone,
    configs,
)

drone_configs = configs.load_drone_config()
llm_configs = configs.load_llm_config()
command_docs = configs.load_command_docs()
command_list = configs.load_command_list()

if __name__ == "__main__":
    # Initialize the drone connection
    drone_connection = drone.Drone(connection_string=drone_configs["connection_string"])
    print("Drone connection established.")

    # Initialize LLM
    llm_model = llm.CohereAPI(
        api_key=llm_configs["api_key"],
        model=llm_configs["model"],
    )

    # Set up RAG (Retrieval-Augmented Generation) documents
    llm_model.set_documents(command_docs)
    print("LLM model initialized with documents.")

    while True:
        input("Press Enter to start listening for a command...")
        raw_command = speech.listen_for_command()

        if raw_command is not None:
            print(f"You said: {raw_command}")

            # Send to LLM
            response = llm_model.send_prompt(
                prompt=llm_configs["prompt_base"] + "\n\nCommand: " + raw_command,
                temperature=llm_configs["temperature"],
                max_tokens=llm_configs["max_tokens"],
                stream=False,
            )

            # Basic cleanup
            response = response.strip().rstrip(".").title()
            print("Response from LLM:", response)

            # Parse response
            response_parts = [part.strip() for part in response.split(",")]
            command = response_parts[0].upper()
            parameters = response_parts[1:]

            if command in command_list:
                print(f"Command: {command}")
                if parameters:
                    print("Parameters:", parameters)
                else:
                    print("No parameters required.")

                try:
                    if command == "TAKEOFF":
                        if len(parameters) != 1:
                            print("Takeoff command requires one parameter: altitude.")
                            continue
                        altitude = float(parameters[0])
                        speech.say(f"Arming drone")
                        drone_connection.arm()
                        speech.say(f"Taking off to {altitude} meters")
                        drone_connection.takeoff(altitude)

                    elif command == "LAND":
                        speech.say("Landing drone in place")
                        drone_connection.land()

                    elif command == "TRAVEL RELATIVE":
                        if len(parameters) != 3:
                            print("Travel Relative requires three parameters: x, y, z.")
                            continue
                        x, y, z = map(float, parameters)
                        
                        speech.say(f"Traveling relative using vector ({x}, {y}, {z})")
                        drone_connection.travel_relative(x, y, z)

                    elif command == "TRAVEL ABSOLUTE":
                        if len(parameters) != 3:
                            print("Travel Absolute requires three parameters: lat, long, alt.")
                            continue
                        lat, lon, alt = map(float, parameters)
                        
                        speech.say(f"Traveling to absolute coordinates ({lat}, {lon}, {alt})")
                        drone_connection.travel_absolute(lat, lon, alt)
                        
                    elif command == "YAW RELATIVE":
                        if len(parameters) != 1:
                            print("Yaw Relative requires one parameter: angle.")
                            continue
                        angle = float(parameters[0])
                        
                        speech.say(f"Yawing relative by {angle} degrees")
                        drone_connection.yaw_relative(angle)
                        
                    elif command == "YAW ABSOLUTE":
                        if len(parameters) != 1:
                            print("Yaw Absolute requires one parameter: angle.")
                            continue
                        angle = float(parameters[0])
                        
                        speech.say(f"Yawing absolute to {angle} degrees")
                        drone_connection.yaw_absolute(angle)

                    elif command == "RTL":
                        speech.say("Returning to Launch")
                        drone_connection.rtl()

                except ValueError:
                    print("Error: Invalid parameter(s). Please ensure numerical values are used.")

            else:
                print("Command not recognized.")
        else:
            print("No command recognized.")
