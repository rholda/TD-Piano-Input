# me - this DAT
# op - the OP which is cooking

def onSetupParameters(op):
    page = op.appendCustomPage('Custom')
    p = page.appendInt('Midichan', label='Midi Channel')
    p.min = 0
    p.max = 16
    p.normMin = p.min
    p.normMax = p.max
    p.clampMin = True
    p.clampMax = True

    p = page.appendInt('Highkey', label='High Key')
    p.min = 0
    p.max = 88
    p.normMin = p.min
    p.normMax = p.max

    p = page.appendInt('Lowkey', label='Low Key')
    p.min = 0
    p.max = 88
    p.normMin = p.min
    p.normMax = p.max

    return

def init(op):
    op.clear()
    key_count = op.par.Highkey.eval() - op.par.Lowkey.eval()
    # print(f'init key_count: {key_count}')
    # Create a channel for each key with a default value of 0
    for key in range(key_count):
        chan = op.appendChan(f'key_{key}')
        chan.vals = [0]

def onCook(op):
    input_chop = op.inputs[0]
    midi_chan = op.par.Midichan.eval()
    high_key = op.par.Highkey.eval()
    low_key = op.par.Lowkey.eval()
    key_count = high_key - low_key
    # Initialize channels if not already done
    if len(op.chans()) != key_count:
        init(op)

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
                        note_num = int(chan_parts[1]) - low_key - 24
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