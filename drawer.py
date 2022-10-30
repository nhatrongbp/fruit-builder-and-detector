import cv2


def draw_button(src, top_left, bottom_right, radius=1, color=(0, 255, 0), thickness=1, line_type=cv2.LINE_AA):

    #  corners:
    #  p1 - p2
    #  |     |
    #  p4 - p3

    p1 = top_left
    p2 = (bottom_right[1], top_left[1])
    p3 = (bottom_right[1], bottom_right[0])
    p4 = (top_left[0], bottom_right[0])

    height = abs(bottom_right[0] - top_left[1])

    if radius > 1:
        radius = 1

    corner_radius = int(radius * (height/4))
    # corner_radius = int(1 * (height/radius))

    if thickness < 0:
        # big rect
        top_left_main_rect = (int(p1[0] + corner_radius), int(p1[1]))
        bottom_right_main_rect = (int(p3[0] - corner_radius), int(p3[1]))

        top_left_rect_left = (p1[0], p1[1] + corner_radius)
        bottom_right_rect_left = (p4[0] + corner_radius, p4[1] - corner_radius)

        top_left_rect_right = (p2[0] - corner_radius, p2[1] + corner_radius)
        bottom_right_rect_right = (p3[0], p3[1] - corner_radius)

        all_rects = [
            [top_left_main_rect, bottom_right_main_rect],
            [top_left_rect_left, bottom_right_rect_left],
            [top_left_rect_right, bottom_right_rect_right]
        ]

        [cv2.rectangle(src, rect[0], rect[1], color, thickness) for rect in all_rects]

    # draw straight lines
    cv2.line(src, (p1[0] + corner_radius, p1[1]), (p2[0] - corner_radius, p2[1]), color, abs(thickness), line_type)
    cv2.line(src, (p2[0], p2[1] + corner_radius), (p3[0], p3[1] - corner_radius), color, abs(thickness), line_type)
    cv2.line(src, (p3[0] - corner_radius, p4[1]), (p4[0] + corner_radius, p3[1]), color, abs(thickness), line_type)
    cv2.line(src, (p4[0], p4[1] - corner_radius), (p1[0], p1[1] + corner_radius), color, abs(thickness), line_type)

    # draw arcs
    cv2.ellipse(src, (p1[0] + corner_radius, p1[1] + corner_radius), (corner_radius, corner_radius), 180.0, 0, 90,
                color, thickness, line_type)
    cv2.ellipse(src, (p2[0] - corner_radius, p2[1] + corner_radius), (corner_radius, corner_radius), 270.0, 0, 90,
                color, thickness, line_type)
    cv2.ellipse(src, (p3[0] - corner_radius, p3[1] - corner_radius), (corner_radius, corner_radius), 0.0, 0, 90,
                color, thickness, line_type)
    cv2.ellipse(src, (p4[0] + corner_radius, p4[1] - corner_radius), (corner_radius, corner_radius), 90.0, 0, 90,
                color, thickness, line_type)

    return src


def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


def draw_gui(screen, drawing, mode, x_pt, y_pt, xx, yy):
    font = cv2.FONT_HERSHEY_DUPLEX
    if drawing:
        draw_border(screen, (min(x_pt, xx), min(y_pt, yy)),
                    (min(x_pt, xx) + abs(xx - x_pt), min(y_pt, yy) + abs(yy - y_pt)),
                    (0, 255, 0), 2, 5, 10)

    cv2.putText(screen, "ONLINE FRUIT DETECTOR B19DC PT081", (50, 50), font, 1, (0, 0, 0), 1)
    cv2.rectangle(screen, (50, 100), (980, 680), (0, 0, 0), 2)
    cv2.rectangle(screen, (1030, 100), (1230, 300), (0, 0, 0), 2)
    cv2.rectangle(screen, (1030, 400), (1230, 680), (255, 255, 255), -1)

    if (1030 < xx < 1230 and 400 < yy < 450) or mode == "manual":
        draw_button(screen, (1030, 400), (450, 1230), radius=0.75, thickness=-1)
        cv2.putText(screen, "MANUAL", (1082, 435), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    else:
        draw_button(screen, (1030, 400), (450, 1230), radius=0.75, thickness=1)
        cv2.putText(screen, "MANUAL", (1082, 435), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    if (1030 < xx < 1230 and 470 < yy < 520) or mode == "auto":
        draw_button(screen, (1030, 470), (520, 1230), radius=0.75, thickness=-1)
        cv2.putText(screen, "AUTOMATIC", (1062, 505), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    else:
        draw_button(screen, (1030, 470), (520, 1230), radius=0.75, thickness=1)
        cv2.putText(screen, "AUTOMATIC", (1062, 505), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    if (1030 < xx < 1230 and 540 < yy < 590) or mode == "preprocessed":
        draw_button(screen, (1030, 540), (590, 1230), radius=0.75, thickness=-1)
        cv2.putText(screen, "PREPROCESSED", (1040, 575), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
    else:
        draw_button(screen, (1030, 540), (590, 1230), radius=0.75, thickness=1)
        cv2.putText(screen, "PREPROCESSED", (1040, 575), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

    if 1030 < xx < 1230 and 630 < yy < 680:
        draw_button(screen, (1030, 630), (680, 1230), color=255, radius=0.75, thickness=-1)
        cv2.putText(screen, "UPLOAD", (1095, 662), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        cv2.line(screen, (1075, 647), (1075, 662), (255, 255, 255), 2)
        cv2.line(screen, (1075, 647), (1070, 652), (255, 255, 255), 2)
        cv2.line(screen, (1075, 647), (1080, 652), (255, 255, 255), 2)
    else:
        draw_button(screen, (1030, 630), (680, 1230), color=255, radius=0.75, thickness=1)
        cv2.putText(screen, "UPLOAD", (1095, 662), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
        cv2.line(screen, (1075, 647), (1075, 662), 255, 2)
        cv2.line(screen, (1075, 647), (1070, 652), 255, 2)
        cv2.line(screen, (1075, 647), (1080, 652), 255, 2)
    cv2.imshow('Frame', screen)
