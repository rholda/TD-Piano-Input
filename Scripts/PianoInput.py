# me - this DAT
# op - the OP which is cooking

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(op):
    page = op.appendCustomPage('Custom')
    p = page.appendInt('Midichan', label='Midi Channel')
    p.min = 0
    p.max = 16
    p.normMin = p.min
    p.normMax = p.max
    p.clampMin = True
    p.clampMax = True

    p = page.appendInt('Keycount', label='Key Count')
    p.min = 12
    p.max = 88
    p.normMin = p.min
    p.normMax = p.max
    p.clampMin = True
    p.clampMax = True

    p = page.appendInt('Rootkey', label='Root Key')
    p.min = 0
    p.max = 88
    p.normMin = p.min
    p.normMax = p.max

    return

def initializeChannels(op):
    op.clear()
    key_count = op.par.Keycount.eval()
    print(f'Set Keys: {key_count}')
    # Create a channel for each key with a default value of 0
    for key in range(key_count):
        chan = op.appendChan(f'key_{key}')
        chan.vals = [0]

def onCook(op):
    input_chop = op.inputs[0]  # Get the input CHOP

    # Initialize channels if not already done
    if len(op.chans()) != int(op.par.Keycount.eval()):
        initializeChannels(op)

    root_key = op.par.Rootkey.eval()
    midi_chan = op.par.Midichan.eval()
    
    # Loop through the channels of the input CHOP
    for i in range(input_chop.numChans):
        try:
            chan_name = input_chop.chan(i).name
            # Only process and output channels that contain 'n' and can be converted to note numbers
            if 'n' in chan_name:
                try:
                    # Extract the MIDI channel from the channel name
                    chan_parts = chan_name.split('n')
                    if len(chan_parts) < 2:
                        continue
                    midi_channel = int(chan_parts[0][2:])  # Extract the MIDI channel number

                    # Check if the MIDI channel matches or if Midichan is 0
                    if midi_chan == 0 or midi_channel == midi_chan:
                        note_num = int(chan_parts[1]) - root_key - 24
                        # Update the corresponding channel if the note number is within the key count
                        if 0 <= note_num < len(op.chans()):
                            op.chans()[note_num].vals = input_chop.chan(i).vals

                except ValueError:
                    # Skip if we can't convert to integer
                    continue
            
        except Exception as e:
            # Print error message to textport for debugging
            print(f"Error processing channel {input_chop.chan(i).name}: {str(e)}")
    
    return