//
//  main.m
//  nsrequest
//
//  Created by Reorx on 16-1-13.
//  Copyright © 2016年 Reorx. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "STHTTPRequest.h"

#define NSCLog(FORMAT, ...) printf("%s\n", [[NSString stringWithFormat:FORMAT, ##__VA_ARGS__] UTF8String]);

#define SYNCHRONOUS 0

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSString *url;
        if (argc > 1) {
            url = [NSString stringWithFormat:@"%s", argv[1]];
        } else {
            url = @"http://ip.cn";
        }
        // NSLog(@"%@", url);
        STHTTPRequest *r = [STHTTPRequest requestWithURLString:url];
        [r setHeaderWithName:@"User-Agent" value:@"curl/7.43.0"];
#if SYNCHRONOUS
        NSError *error = nil;
        [r startSynchronousWithError:&error];
        NSLog(@"--> %@", r.responseString);
#else
        r.completionBlock = ^(NSDictionary *headers, NSString *body) {
            NSCLog(@"%@", body);
            exit(0);
        };
        
        r.errorBlock = ^(NSError *error) {
            NSCLog(@"%@", error);
            exit(1);
        };
        
        [r startAsynchronous];
        
        [[NSRunLoop currentRunLoop] run];
#endif
    }
    return 0;
}
