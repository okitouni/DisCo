import tensorflow as tf

def distance_corr(var_1, var_2, normedweight, power=1):
    """var_1: First variable to decorrelate (eg mass)
    var_2: Second variable to decorrelate (eg classifier output)
    normedweight: Per-example weight. Sum of weights should add up to 1
    power: Exponent used in calculating the distance correlation
    
    va1_1, var_2 and normedweight should all be 1D torch tensors with the same number of entries
    
    Usage: Add to your loss function. total_loss = BCE_loss + lambda * distance_corr
    """

    xx = tf.reshape(var_1, [-1, 1])
    xx = tf.tile(xx, [1, len(var_1)])
    xx = tf.reshape(xx, [len(var_1), len(var_1)])
    
    yy = tf.tile(var_1, [len(var_1)])
    yy = tf.reshape(yy, [len(var_1), len(var_1)])
    amat = tf.math.abs(xx-yy)
    
    xx = tf.reshape(var_2, [-1, 1])
    xx = tf.tile(xx, [1, len(var_2)])
    xx = tf.reshape(xx, [len(var_2), len(var_2)])
    
    yy = tf.tile(var_2, [len(var_2)])
    yy = tf.reshape(yy, [len(var_2), len(var_2)])
    bmat = tf.math.abs(xx-yy)
    
    amatavg = tf.reduce_mean(amat*normedweight, axis=1)
    bmatavg = tf.reduce_mean(bmat*normedweight, axis=1)
    
    minuend_1 = tf.tile(amatavg, [len(var_1)])
    minuend_1 = tf.reshape(minuend_1, [len(var_1), len(var_1)])
    minuend_2 = tf.reshape(amatavg, [-1, 1])
    minuend_2 = tf.tile(minuend_2, [1, len(var_1)])
    minuend_2 = tf.reshape(minuend_2, [len(var_1), len(var_1)])
    Amat = amat-minuend_1-minuend_2+tf.reduce_mean(amatavg*normedweight)
    
    minuend_1 = tf.tile(bmatavg, [len(var_2)])
    minuend_1 = tf.reshape(minuend_1, [len(var_2), len(var_2)])
    minuend_2 = tf.reshape(bmatavg, [-1, 1])
    minuend_2 = tf.tile(minuend_2, [1, len(var_2)])
    minuend_2 = tf.reshape(minuend_2, [len(var_2), len(var_2)])
    Bmat = bmat-minuend_1-minuend_2+tf.reduce_mean(bmatavg*normedweight)
    
    ABavg = tf.reduce_mean(Amat*Bmat*normedweight,axis=1)
    AAavg = tf.reduce_mean(Amat*Amat*normedweight,axis=1)
    BBavg = tf.reduce_mean(Bmat*Bmat*normedweight,axis=1)
    
    if power==1:
        dCorr = tf.reduce_mean(ABavg*normedweight)/tf.math.sqrt(tf.reduce_mean(AAavg*normedweight)*tf.reduce_mean(BBavg*normedweight))
    elif power==2:
        dCorr = (tf.reduce_mean(ABavg*normedweight))**2/(tf.reduce_mean(AAavg*normedweight)*tf.reduce_mean(BBavg*normedweight))
    else:
        dCorr = tf.reduce_mean(ABavg*normedweight)/tf.math.sqrt(tf.reduce_mean(AAavg*normedweight)*tf.reduce_mean(BBavg*normedweight))**power

