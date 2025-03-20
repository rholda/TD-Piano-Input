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

    return

def init(op):
    op.clear()
    print(f'Set Sustain Pedal')
    chan = op.appendChan(f'sustain')
    chan.vals = [0]

def onCook(op):
    input_chop = op.inputs[0]  # Get the input CHOP

    # Initialize channels if 'sustain' channel is not found
    if 'sustain' not in [chan.name for chan in op.chans()]:
        init(op)

    sustain_channel = op.chans('sustain')[0]
    midi_chan = op.par.Midichan.eval()
    
    # Check if input_chop has a channel containing 'ctrl64' and set sustain values
    for chan in input_chop.chans():
        if 'ctrl64' in chan.name:
            # Extract the MIDI channel from the channel name
            chan_parts = chan.name.split('ctrl64')
            if len(chan_parts) < 2:
                continue
            midi_channel = int(chan_parts[0][2:])  # Extract the MIDI channel number

            # Check if the MIDI channel matches or if Midichan is 0
            if midi_chan == 0 or midi_channel == midi_chan:
                sustain_channel.vals = chan.vals
                break
    else:
        sustain_channel.vals = [0]

    return